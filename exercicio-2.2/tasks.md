# Tasks — Query Endpoint

> Derivado de `specs/query-endpoint/plan.md`. Local de destino no repo: `specs/query-endpoint/tasks.md`.
> Gerado pelo Dev (com apoio de IA), pendente de aprovação do Tech Lead.
> **Grão de fatiamento:** fatias verticais — cada task termina com o repo verde (compila, testa, roda), não "um arquivo por task".

## Legenda de estimativa
- **P** (Pequeno) — ~até 2h, escopo enxuto.
- **M** (Médio) — ~meio dia, lógica com I/O mockável + testes.
- **G** (Grande) — ~1 dia, várias peças e mocks de API externa.

## Convenções aplicadas a todas as tasks
- TDD: cada fatia entrega o(s) teste(s) da capacidade que ela cria.
- `strict: true` — toda task compila sem `any` implícito.
- APIs Azure são sempre mockadas nesta fase (msw / clientes injetáveis); nenhuma chamada externa real.
- Erros externos nunca vazam segredos no log nem na resposta HTTP.
- **Infra compartilhada cresce por demanda:** `types.ts`, `config.ts`, `errors.ts` nascem mínimos na S-1 e ganham campos nas fatias seguintes; `retry.ts` nasce na S-2; `logger.ts` na S-5. Não há task "criar arquivo X" sem cliente.

---

## S-1 — Endpoint + validação de input
**Arquivos:** `src/functions/query/handler.ts`, `src/functions/query/validator.ts`, `src/shared/types.ts` (mínimo), `src/shared/config.ts` (mínimo), `src/shared/errors.ts` (mínimo), `tests/unit/validator.test.ts`
**Descrição:** Scaffold do HTTP trigger v4 do `POST /api/query` + validação de input com Zod. Cria o mínimo de tipos (`QueryRequest`, `QueryResponse`), config (carregar env com fail-fast) e `ValidationError` que esta fatia exige. O handler ainda **não** chama serviços — devolve uma resposta stub tipada.
**Critérios de aceite:**
- `POST` com body inválido → `400` com o detalhe do campo (`ValidationError`).
- `POST` válido → `200` com resposta stub no shape de `QueryResponse`.
- `config` falha rápido e com mensagem clara se faltar env obrigatória.
- Compila com `strict: true`, sem `any`.
- **Termina rodável:** `npm run build` ok + teste unitário do validator verde.
**Dependências:** —
**Estimativa:** M

## S-2 — Recuperação (embedding + busca top-5)
**Arquivos:** `src/services/completion.ts` (`embedQuery`), `src/services/search.ts`, `src/shared/retry.ts`, `tests/fixtures/chunks.ts`, `tests/fixtures/queries.ts`, `tests/unit/search.test.ts`, `tests/unit/retry.test.ts`
**Descrição:** Gera o embedding da pergunta (Azure OpenAI) e busca os top-5 chunks (Azure AI Search). Inclui o wrapper de retry com backoff exponencial + jitter, usado por ambas as chamadas. Clientes Azure injetáveis para mock.
**Critérios de aceite:**
- `embedQuery` retorna vetor; `search` retorna ≤5 `RetrievalResult` ordenados por score (desc) e `[]` quando não há resultado (sem lançar).
- `retry` re-tenta 429/5xx/timeout, **não** re-tenta 4xx; testado com fake timers.
- Falhas viram `SearchError` / `CompletionError`.
- **Termina rodável:** testes unitários de `search` e `retry` verdes com Azure mockado (msw/stub). Zero chamada externa real.
**Dependências:** S-1 (tipos, errors)
**Estimativa:** G

## S-3 — Montagem do prompt (context budget + vigência)
**Arquivos:** `src/services/prompt-builder.ts`, `tests/fixtures/expected-responses.ts`, caso contraditório adicionado em `tests/fixtures/chunks.ts`, `tests/unit/prompt-builder.test.ts`
**Descrição:** Monta o prompt = system prompt (lido de `/prompts/system-prompt.md`) + chunks recuperados + pergunta, respeitando o context budget (~4K system + ~8K chunks, ADR-0002) e priorizando o documento vigente em contradições (ADR-0003).
**Critérios de aceite:**
- Nunca excede o budget; trunca chunks por menor score primeiro.
- System prompt lido da fonte versionada (não hardcoded).
- Em contradição, chunk vigente prevalece sobre obsoleto.
- **Termina rodável:** teste unitário com fixtures (caso feliz + caso contraditório) verde.
**Dependências:** S-1, S-2 (`RetrievalResult`)
**Estimativa:** M

## S-4 — Completion + resposta com fonte
**Arquivos:** `src/services/completion.ts` (`complete`), `src/functions/query/response-builder.ts`, `tests/unit/response-builder.test.ts`
**Descrição:** Envia o prompt montado ao GPT-4o e monta `QueryResponse` com `source_document` derivado do chunk de maior relevância efetivamente usado.
**Critérios de aceite:**
- `complete` retorna o texto da resposta; usa retry; falha vira `CompletionError`.
- `source_document` presente e rastreável ao chunk de origem.
- **Termina rodável:** teste unitário do `response-builder` verde com completion mockado.
**Dependências:** S-2 (retry, tipos), S-3 (prompt montado)
**Estimativa:** M

## S-5 — Validação determinística da resposta
**Arquivos:** `src/services/response-validator.ts`, `src/shared/logger.ts`, `tests/unit/response-validator.test.ts`
**Descrição:** Harness determinístico: schema Zod de saída + checagem de que existe `source_document` e de que a resposta referencia a fonte. Adiciona o logger estruturado (pino) que o handler usará na fiação final.
**Critérios de aceite:**
- Rejeita resposta sem `source_document` ou fora do schema, retornando erro **estruturado** (não boolean opaco).
- `logger` emite JSON com `requestId`; nível controlado por env.
- **Termina rodável:** teste unitário verde.
**Dependências:** S-1, S-4
**Estimativa:** M

## S-6 — Fiação completa + teste de integração
**Arquivos:** `src/functions/query/handler.ts` (atualiza o stub da S-1), `tests/integration/query.test.ts`
**Descrição:** Substitui o stub do handler pela orquestração real: validar input → embedding → busca → montar prompt → completion → montar resposta → validar resposta, com logging por request e mapeamento de erros → status. Teste de integração com msw e as fixtures acumuladas.
**Critérios de aceite:**
- Caso feliz: `200` com `source_document` correto.
- Caso contraditório: resposta prioriza o documento vigente.
- Caso sem resultado: resposta apropriada (sem `5xx`).
- Input inválido: `400`; falha Azure: `502/504` (mapeado pelos erros).
- **Termina rodável:** suíte de integração verde, sem chamadas externas reais.
**Dependências:** S-1, S-2, S-3, S-4, S-5
**Estimativa:** M

---

## Sequenciamento e caminho crítico
- Fatias são lineares: **S-1 → S-2 → S-3 → S-4 → S-5 → S-6**, cada uma deixando o repo verde.
- A fatia mais pesada é a **S-2** (dois serviços + retry + mocks de duas APIs) — é o ponto natural para revisão de meio de caminho.
- A integração não fica represada no fim: a S-1 já entrega o handler rodando (stub), e a S-6 só troca o miolo. O risco de fiação se distribui em vez de virar um único "G" terminal.

## Cobertura do plan.md
- Passo 1 (receber pergunta + validar) → S-1
- Passo 2 (embedding) → S-2
- Passo 3 (top-5 chunks) → S-2
- Passo 4 (montar prompt + budget) → S-3
- Passo 5 (GPT-4o + resposta com fonte) → S-4, S-5
- Decisões técnicas (Zod / retry / pino) → S-1, S-2, S-5
- Dependências externas do plan (índice populado, system prompt finalizado) → pré-requisitos das fatias, não tasks deste módulo.
