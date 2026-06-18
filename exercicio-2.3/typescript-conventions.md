---
name: typescript-conventions
description: "Ao escrever ou revisar qualquer código TypeScript do projeto."
---

# TypeScript Conventions

## Contexto

Esta skill define a base de tipagem do projeto NovaTech. Ela governa como modelamos contratos, nomeamos símbolos, organizamos módulos e evitamos brechas de tipagem que passam no compilador, mas quebram em runtime.

`strict` já está ativo no projeto (`tsconfig.json`), então as regras abaixo partem desse contrato. As convenções foram extraídas do código existente (`src/shared/types.ts`, `src/functions/query/`); os exemplos seguem a formatação do codebase (indentação de 2 espaços) e importam contratos compartilhados de `src/shared/types.ts` em vez de redeclará-los.

Nota explícita: esta skill é BASE. As outras skills assumem estas regras e não devem reescrevê-las.

Quando um tópico sair do escopo de TypeScript puro, referencie a skill irmã adequada:
- tratamento de erro: `foundation/error-handling.md`
- logging/observabilidade: `foundation/logging-observability.md`
- configuração de ambiente e validação de env: `foundation/env-config.md`

## Regras Prescritivas

1. Use tipagem explícita em fronteiras de entrada e saída (handlers, validators, services, builders).
2. Nunca use `any`; prefira `unknown` na entrada não confiável e refine com validação/type guards.
3. Use `interface` para contratos de objeto (DTOs e modelos de domínio), espelhando `src/shared/types.ts`. Use `type` para unions literais, aliases, intersections e tipos utilitários/mapeados.
4. Use camelCase em identificadores internos (funções, variáveis, parâmetros), PascalCase em tipos/interfaces e UPPER_SNAKE_CASE em constantes globais. **Exceção:** campos de um contrato externo (resposta JSON) seguem o contrato de fio — no projeto isso é snake_case (ex.: `source_document`, `relevance_score`). Não renomeie esses campos para camelCase no TS sem mudar o contrato.
5. Use unions literais para domínios fechados (ex.: ambientes e níveis), evitando `string` genérico. A lista autoritativa de ambientes (`development | staging | production`) e sua validação pertencem a `foundation/env-config.md`.
6. Use `readonly` em propriedades de contrato de saída que não devem ser mutadas.
7. Nunca exporte default em módulo de domínio; use exports nomeados para facilitar refatoração e rastreabilidade.
8. Nunca use barrel global que mistura camadas; exporte por módulo e mantenha imports explícitos.
9. Nunca force tipo com `as` para "calar" o compilador em dados de runtime (env, payload HTTP, resposta externa).
10. Use type assertion (`as`) somente quando houver garantia local e documentada (ex.: narrowing por guard, API interna estritamente controlada).
11. Prefira pequenas funções de refinamento de tipo (`isX`) para tornar suposições de runtime explícitas.
12. Contratos compartilhados entre camadas vivem em `src/shared/types.ts`; importe de lá em vez de redeclarar.

## Exemplos DO/DON'T

### 1) Entrada HTTP: `unknown` + validação (não `any`)

DON'T

```ts
export function validateQueryRequest(input: any): QueryRequest {
  return {
    query: input.query,
  };
}
```

DO

```ts
import { z } from "zod";
import type { QueryRequest } from "../../shared/types";

const QueryRequestSchema = z.object({
  query: z.string().min(5).max(1000),
});

export function validateQueryRequest(input: unknown): QueryRequest {
  return QueryRequestSchema.parse(input);
}
```

### 2) Domínio fechado: union literal + `interface` (não `string` genérico)

DON'T

```ts
interface AppConfig {
  environment: string;
  logLevel: string;
}
```

DO

```ts
type Environment = "development" | "staging" | "production";
type LogLevel = "debug" | "info" | "warn" | "error";

interface AppConfig {
  readonly environment: Environment;
  readonly logLevel: LogLevel;
}
```

### 3) Assertions: só com garantia local

DON'T

```ts
const environment = (process.env.NODE_ENV || "development") as
  | "development"
  | "production";
```

DO

```ts
type Environment = "development" | "staging" | "production";

function isEnvironment(value: string): value is Environment {
  return value === "development" || value === "staging" || value === "production";
}

function parseEnvironment(value: string | undefined): Environment {
  const candidate = value ?? "development";
  if (!isEnvironment(candidate)) {
    throw new Error(`NODE_ENV inválido para o contrato esperado: ${candidate}`);
  }
  return candidate;
}

const environment = parseEnvironment(process.env.NODE_ENV);
```

Observação: a regra de fail-fast e a validação completa de env (incluindo quais variáveis são obrigatórias) pertencem à `foundation/env-config.md`.

### 4) Export de módulo: nomeado + tipo compartilhado importado (não default, não redeclarado)

DON'T

```ts
export default function buildQueryResponse(answer: string) {
  return {
    response: answer,
    source_document: {
      id: "doc-001",
      title: "POL-001",
      url: "https://novatech/policies/pol-001",
      relevance_score: 0.92,
    },
  };
}
```

DO

```ts
import type { QueryResponse, SourceDocument } from "../../shared/types";

// Recebe a fonte recuperada em vez de fabricá-la; o shape vive em shared/types.ts.
export function buildQueryResponse(answer: string, source: SourceDocument): QueryResponse {
  return {
    response: answer,
    source_document: source,
  };
}
```

## Anti-padrões

- Usar `any` em payload HTTP ou integração externa: remove a segurança de `strict` e mascara regressões de contrato.
- Usar `as` para forçar tipos de dados de runtime sem validação: cria falsa sensação de segurança e desloca o erro para produção. Exemplo recorrente da S-1: cast direto de `process.env` para union em config (`as "development" | "production"`) sem prova de runtime — que, de quebra, escondeu a ausência de `staging` no domínio.
- Redeclarar localmente um contrato que já existe em `src/shared/types.ts`: gera divergência silenciosa entre cópias. Importe o tipo.
- Renomear campos do contrato externo para camelCase só por estética (ex.: `source_document` → `sourceDocument`): quebra o contrato de fio com os consumidores.
- Misturar regra de tipagem com regra de negócio/erro no mesmo utilitário: dificulta reuso e viola a separação entre skills Foundation.
- Export default em módulo de domínio compartilhado: dificulta busca estática, auto-import e refatoração segura.
