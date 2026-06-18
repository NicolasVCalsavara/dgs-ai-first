# Árvore de Skills — NovaTech Assistant

> **Conceito.** Skills são artefatos estruturados (`.md`) que encapsulam *como gerar* um tipo de output.
> Hierarquia: **Foundation** (convenções globais) → **Domain** (padrões por camada) → **Artifact** (receitas de geração).
> A composição é **para baixo**: uma skill Artifact referencia skills Domain, que referenciam skills Foundation. Uma convenção vive em **um único lugar** e é reusada por referência — nunca copiada.

---

## Visão da árvore

```
skills/
├── foundation/                      # convenções globais — agnósticas de artefato, mudam raramente
│   ├── typescript-conventions.md    # [existe]  strict, sem any, naming, exports/módulos
│   ├── error-handling.md            # [existe]  erros tipados, mapeamento → HTTP, mensagens PT-BR, nunca vazar segredo
│   ├── logging-observability.md     # [novo]    pino estruturado, requestId, redaction, o que (não) logar
│   ├── env-config.md                # [novo]    carga/validação de env com Zod, fail-fast, ambientes dev/staging/prod
│   ├── testing-conventions.md       # [novo]    AAA, naming, asserções que SEMPRE executam (sem false-green)
│   └── project-structure.md         # [existe]  layout de pastas, slugs, fronteiras de import
│
├── domain/                          # padrões por camada/tecnologia — mudam ocasionalmente
│   ├── azure-functions-endpoint.md  # [existe]  anatomia do HTTP trigger v4: handler+validator+response-builder, erro→status, DI
│   ├── rag-query-pattern.md         # [novo]    fluxo RAG: validar→embed→search→prompt(budget/vigência)→complete→validar→source_document
│   ├── azure-ai-search-integration.md # [existe] embeddings, top-k, retry/backoff, mock via msw
│   ├── testing-patterns.md          # [existe]  unit vs integration vs e2e, fixtures (chunks/queries/expected), mock de Azure
│   ├── react-components.md          # [existe]  organização do painel: props tipadas, estado, design tokens, acessibilidade
│   ├── technical-documentation.md   # [novo]    convenções de ADR (NNNN-titulo, Contexto/Decisão/Consequências/Alternativas) e README de módulo
│   └── sdd-spec-authoring.md        # [novo]    método SDD: requirements/plan/tasks, grão de task = fatia vertical, critérios de aceite
│
└── artifact/                        # receitas de geração — o que o dev/agente invoca; evoluem conforme o padrão amadurece
    ├── create-rag-endpoint.md       # [existe]  gera um endpoint RAG completo + sua suíte
    ├── create-integration-test.md   # [existe]  gera suíte de integração de endpoint (msw + fixtures + casos)
    ├── create-react-card.md         # [existe]  gera um card de resposta do painel
    ├── create-feedback-form.md      # [novo]    gera um formulário de feedback
    ├── create-adr.md                # [novo]    gera um ADR a partir do template
    ├── create-module-readme.md      # [novo]    gera o README de um módulo
    └── create-spec.md               # [novo]    gera o trio SDD (requirements/plan/tasks) de um módulo
```

---

## Foundation — convenções globais

Aplicam-se a **todo** artefato do projeto. São folhas: não dependem de nenhuma outra skill.

| Skill | Encapsula |
|---|---|
| `typescript-conventions` | `strict: true`, proibição de `any`, convenção de nomes, organização de exports e módulos. |
| `error-handling` | Hierarquia de erros tipados, `statusCode` por erro, **mensagens ao usuário em PT-BR**, regra de nunca vazar segredo/stack na resposta. |
| `logging-observability` | Logger pino estruturado (JSON), correlação por `requestId`, redaction de campos sensíveis, níveis por env. |
| `env-config` | Carga e validação de env com Zod, **fail-fast em variável obrigatória ausente**, contrato de config, ambientes `dev`/`staging`/`prod`. |
| `testing-conventions` | AAA, naming, e a regra de ouro: **toda asserção precisa executar** (`expect.assertions`/`expect.fail`) — nada de verificação enterrada em `catch`/`if`. |
| `project-structure` | Onde cada coisa mora (`src/functions`, `services`, `shared`, `tests`), slugs de pasta, fronteiras de import. |

---

## Domain — padrões por camada

Descrevem *como* uma camada é construída. Cada uma **referencia** as Foundation que pressupõe.

| Skill | Encapsula | Apoia-se em (Foundation) |
|---|---|---|
| `azure-functions-endpoint` | Anatomia do HTTP trigger v4: handler + validator + response-builder, mapeamento erro→status, dependências injetáveis. | error-handling, logging-observability, env-config, project-structure |
| `rag-query-pattern` | O fluxo RAG reutilizável: validar → embed → search → montar prompt (budget ADR-0002, vigência ADR-0003) → completar → validar resposta → `source_document`. | error-handling, env-config |
| `azure-ai-search-integration` | Geração de embedding, busca top-k, retry/backoff, mock via msw. | error-handling, env-config |
| `testing-patterns` | Fronteiras unit/integration/e2e, fixtures compartilhadas (chunks/queries/expected), como mockar Azure. | testing-conventions, project-structure |
| `react-components` | Organização dos componentes do painel: props tipadas, estado, design tokens, acessibilidade. | typescript-conventions |
| `technical-documentation` | Formato de ADR (`NNNN-titulo`, Contexto/Decisão/Consequências/Alternativas) e estrutura de README de módulo. | project-structure |
| `sdd-spec-authoring` | Método SDD: o trio requirements/plan/tasks, grão de task como **fatia vertical** que termina rodável, formato de critérios de aceite. | project-structure |

---

## Artifact — receitas de geração

São os **pontos de entrada**: o que o dev (ou o agente) invoca para produzir um artefato concreto. Cada receita *puxa a cadeia* de Domain + Foundation — sem reescrever as regras.

| Receita | Produz | Compõe (Domain) |
|---|---|---|
| `create-rag-endpoint` | Um endpoint RAG completo (handler, validator, services, response-builder) + suíte. | azure-functions-endpoint, rag-query-pattern, azure-ai-search-integration, testing-patterns |
| `create-integration-test` | Suíte de integração de um endpoint: msw + fixtures + casos (feliz / contraditório / vazio / inválido). | testing-patterns |
| `create-react-card` | Um card de resposta do painel. | react-components |
| `create-feedback-form` | Um formulário de feedback do painel. | react-components |
| `create-adr` | Um ADR preenchido a partir do template. | technical-documentation |
| `create-module-readme` | O README de um módulo. | technical-documentation |
| `create-spec` | O trio SDD de um módulo (requirements pelo PM, plan pelo TL, tasks pelo Dev). | sdd-spec-authoring |

---

## Mapa: artefato recorrente → receita Artifact

| Artefato recorrente do projeto | Receita(s) |
|---|---|
| Endpoints Azure Functions com padrão RAG | `create-rag-endpoint` |
| Testes de integração para endpoints | `create-integration-test` |
| Componentes React (cards, formulários de feedback) | `create-react-card`, `create-feedback-form` |
| Documentação técnica (ADRs, README de módulos) | `create-adr`, `create-module-readme` |
| Specs de produto (template SDD) | `create-spec` |

---

## Modelo de composição

```
Artifact  →  Domain  →  Foundation
(receita)    (padrão)    (convenção)

create-rag-endpoint
   ├── azure-functions-endpoint ─┬─ error-handling
   │                             ├─ logging-observability
   │                             ├─ env-config
   │                             └─ project-structure
   ├── rag-query-pattern ────────┬─ error-handling
   │                             └─ env-config
   ├── azure-ai-search-integration ─ (mesmas Foundation)
   └── testing-patterns ─────────┬─ testing-conventions
                                 └─ project-structure
```

Regra prática: se uma receita Artifact está repetindo texto de regra (ex.: "use erros tipados, não vaze segredo"), isso é sinal de que a regra deveria estar numa Foundation/Domain e ser **referenciada**, não copiada.

---

## Princípios de design da árvore

1. **DRY para baixo.** Cada convenção existe em exatamente um lugar (Foundation). Mudou o padrão de erro? Edita-se `error-handling` e todas as receitas herdam.
2. **Artifact é entrada, Foundation é base.** O dev/agente invoca uma receita Artifact; a cadeia Domain→Foundation vem junto por referência.
3. **Estabilidade por camada.** Foundation muda raramente, Domain ocasionalmente, Artifact evolui à medida que o padrão amadurece. Quem muda mais fica mais perto da folha de invocação.
4. **Composição, não duplicação.** Receitas referenciam skills; não reescrevem suas regras.
5. **As skills capturam lições, não só ideais.** `env-config` e `testing-conventions` nasceram exatamente dos dois defeitos bloqueantes da revisão da S-1 (config sem fail-fast / que quebra em `staging`; e testes false-green). Codificá-los como Foundation impede que se repitam no próximo endpoint.

---

## Estado vs. a criar

- **Já existem como placeholder** (Anexo C): 3 Foundation, 4 Domain, 3 Artifact — arquivos criados, conteúdo a escrever.
- **A criar nesta árvore:** Foundation `logging-observability`, `env-config`, `testing-conventions`; Domain `rag-query-pattern`, `technical-documentation`, `sdd-spec-authoring`; Artifact `create-feedback-form`, `create-adr`, `create-module-readme`, `create-spec`.

Ordem sugerida de escrita: Foundation primeiro (são base de todo o resto), depois as Domain mais usadas (`azure-functions-endpoint`, `rag-query-pattern`, `testing-patterns`), e por fim a receita `create-rag-endpoint` — que é a que mais se paga, dado que "vários endpoints RAG" é o artefato mais repetido do projeto.
