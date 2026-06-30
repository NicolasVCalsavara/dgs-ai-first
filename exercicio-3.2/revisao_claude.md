# Revisão de Código — `feedback-handler.ts`

> Code review do handler gerado pelo Copilot, à luz do `AGENTS.md` do projeto NovaTech Assistant.
> Problemas classificados em: **violação do AGENTS.md**, **problema de segurança** e **bug potencial**. Alguns itens se enquadram em mais de uma categoria — indicado quando aplicável.

## Regras de referência (resumo do AGENTS.md)

- TypeScript strict mode
- Zod para validação de input
- pino para logging (nunca `console.log`)
- Nunca logar dados pessoais (e-mail, nome)
- Imports estáticos no topo (nunca `require` dinâmico)

---

## Violações do AGENTS.md

| # | Problema | Trecho | Correção esperada |
|---|----------|--------|-------------------|
| 1 | `require` dinâmico dentro da função | `const { CosmosClient } = require('@azure/cosmos')` | `import { CosmosClient } from '@azure/cosmos'` no topo do arquivo |
| 2 | Uso de `console.log` | `console.log('Feedback recebido:', ...)` | Usar o logger de `src/shared/logger.ts` (pino) |
| 3 | Log de dado pessoal | O log serializa o objeto inteiro, incluindo `attendantEmail` | Remover PII do log; mesmo com pino, o e-mail não pode entrar no log |
| 4 | Sem validação Zod | `body.queryId`, `body.rating`, `body.comment`, `body.attendantEmail` lidos direto | Validar com schema Zod em `src/functions/feedback/validator.ts` |
| 5 | Uso de `as any` | `await request.json() as any` | Tipo derivado de `schema.parse()`, eliminando o `any` e respeitando `strict: true` |

---

## Problemas de segurança

| # | Problema | Detalhe | Correção esperada |
|---|----------|---------|-------------------|
| 6 | PII em log *(também item 3)* | E-mail do atendente em texto claro em qualquer sink (App Insights, stdout) | Nunca registrar `attendantEmail` |
| 7 | Endpoint sem autenticação | `app.http` usa `authLevel: 'anonymous'` por padrão; qualquer um pode gravar no Cosmos | Definir `authLevel` ou proteger por outra via |
| 8 | Entrada não validada e persistida | `comment` aceita qualquer tamanho/conteúdo e é gravado como veio → risco de XSS armazenado se o painel-web renderizar sem escapar | Validar e sanitizar via Zod antes de persistir |

---

## Bugs potenciais

| # | Problema | Detalhe | Correção esperada |
|---|----------|---------|-------------------|
| 9 | `request.json()` sem try/catch | Corpo malformado lança exceção não tratada → 500 cru | Tratar e retornar 400 controlado |
| 10 | Connection string possivelmente `undefined` | `process.env.COSMOS_CONNECTION_STRING` não verificado | Carregar de `src/shared/config.ts` com validação na inicialização |
| 11 | `CosmosClient` instanciado a cada request | Client + database + container criados dentro do handler em toda requisição → desperdício e risco de esgotar conexões sob carga | Criar o client uma vez em escopo de módulo |
| 12 | `container.items.create` sem tratamento de erro | Falha do Cosmos (throttling 429, indisponibilidade) borbulha como 500 sem log nem resposta adequada | Envolver em try/catch com log e resposta apropriada |
| 13 | `rating` sem checagem de domínio | Nada garante faixa válida (ex: 1–5); dado inconsistente entra na base | Validar domínio via Zod *(relacionado ao item 4)* |

---

## Causa raiz

O Copilot ignorou a estrutura que o projeto já prevê — `validator.ts` (Zod), `shared/logger.ts` (pino) e `shared/config.ts` — e gerou um handler "solto", concentrando toda a lógica no arquivo sem reaproveitar as convenções do repositório.

## Próximos passos sugeridos

1. Mover imports para o topo (estáticos).
2. Criar o schema Zod em `src/functions/feedback/validator.ts` e derivar o tipo dele.
3. Substituir `console.log` por pino, sem PII.
4. Instanciar o `CosmosClient` em escopo de módulo, com connection string vinda de `config.ts`.
5. Envolver parsing e persistência em try/catch com respostas 400/500 controladas.
6. Definir `authLevel` no `app.http`.
