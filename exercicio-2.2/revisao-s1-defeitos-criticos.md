## Defeito #1 — A suíte de testes passa sem testar (false green)

### Descrição
Vários testes colocam as asserções relevantes dentro de `try/catch` + `if (error instanceof ...)`:

```ts
expect(() => validateQueryRequest(input)).toThrow(ValidationError);
try {
  validateQueryRequest(input);
} catch (error) {
  if (error instanceof ValidationError) {
    expect(error.details.query[0]).toContain("...");
  }
}
```

Se a função deixar de lançar — ou lançar outro tipo de erro — o bloco `catch`/`if` é pulado **silenciosamente** e o teste fica verde sem ter executado nenhuma asserção.

O caso mais grave é `"should return ValidationError with 400 status code"`, que **não tem** o `expect(...).toThrow()` externo: toda a sua verificação vive dentro do `catch`. Se a validação não disparar, ele não testa absolutamente nada.

### Evidência (teste de mutação)
Removendo a regra `.min(5)` do validator:

```
× should reject query that is too short
× should reject query field that is an empty string
✓ should return ValidationError with 400 status code   ← continuou VERDE com o código quebrado
... (7 passaram, 2 falharam)
```

Com `{ query: "x" }` deixando de lançar, o `catch` nunca rodou e o teste de status 400 passou mesmo assim.

### Correção recomendada
Garantir que o caminho de asserção sempre execute. Duas formas idiomáticas no Vitest:

```ts
// Opção A — força a contagem de asserções
it("should return ValidationError with 400 status code", () => {
  expect.assertions(2);
  try {
    validateQueryRequest({ query: "x" });
  } catch (error) {
    expect(error).toBeInstanceOf(ValidationError);
    expect((error as ValidationError).statusCode).toBe(400);
  }
});

// Opção B — falha explícita se não lançar
it("should return ValidationError with 400 status code", () => {
  try {
    validateQueryRequest({ query: "x" });
    expect.fail("deveria ter lançado ValidationError");
  } catch (error) {
    expect(error).toBeInstanceOf(ValidationError);
    expect((error as ValidationError).statusCode).toBe(400);
  }
});
```

Aplicar o mesmo princípio a todos os testes que hoje inspecionam o erro dentro de `if (error instanceof ...)`.

---

## Defeito #2 — `config` com fail-fast decorativo e que quebra em ambiente válido

### Descrição
O critério de aceite da S-1 diz: *"config falha rápido e com mensagem clara se faltar env obrigatória"*. Porém **nenhuma variável é obrigatória** — tanto `NODE_ENV` quanto `LOG_LEVEL` têm fallback (`|| "development"`, `|| "info"`). Logo, o fail-fast nunca dispara por variável ausente: o critério está, na prática, **não atendido**.

Pior: a única validação existente derruba a aplicação num ambiente legítimo do próprio projeto. O `config` aceita apenas `development | production`, mas o repositório tem `infra/parameters/staging.bicepparam` — **staging é um ambiente real**. Como a config é executada no import (`export const config = loadConfig()`), o erro acontece já na carga do módulo (crash opaco do worker no Azure Functions host, e difícil de testar isoladamente). Além disso, lança `Error` cru em vez de um erro tipado coerente com `src/shared/errors.ts`.

### Evidência
```
$ NODE_ENV=staging node -e 'import("./dist/src/shared/config.js")'
THROW no import com NODE_ENV=staging => [Config] NODE_ENV must be 'development' or 'production', got: staging
```

Um deploy de staging legítimo quebra na inicialização.

### Correção recomendada
- Definir o **contrato real** de variáveis (quais são obrigatórias) e validá-lo com Zod, espelhando o validator de input.
- Incluir `staging` na lista de ambientes aceitos.
- Lançar erro **tipado** (`ConfigError`) em vez de `Error`.
- Evitar (ou isolar) a execução no import, para não derrubar a carga do módulo e permitir teste unitário.

```ts
import { z } from "zod";
import { ConfigError } from "./errors";

const ConfigSchema = z.object({
  environment: z.enum(["development", "staging", "production"]).default("development"),
  logLevel: z.enum(["debug", "info", "warn", "error"]).default("info"),
  // declarar aqui as vars REALMENTE obrigatórias quando entrarem (S-2+):
  // azureSearchEndpoint: z.string().url(),
});

export type Config = z.infer<typeof ConfigSchema>;

let cached: Config | null = null;

export function getConfig(): Config {
  if (cached) return cached;
  const result = ConfigSchema.safeParse({
    environment: process.env.NODE_ENV,
    logLevel: process.env.LOG_LEVEL,
  });
  if (!result.success) {
    throw new ConfigError("Configuração de ambiente inválida", result.error.flatten());
  }
  cached = result.data;
  return cached;
}
```
