## 1. Violações de AGENTS.md

### 1.1 Uso de `any` em strict mode
- Burla strict mode
- Remove type narrowing
- Elimina garantias do compilador

---

### 1.2 Ausência de validação com Zod
O código aceita qualquer payload sem validação.

---

### 1.3 Uso de `console.log`
O projeto exige pino.

---

### 1.4 Import dinâmico via require
```ts
const { CosmosClient } = require('@azure/cosmos');
```

Esperado:
```ts
import { CosmosClient } from '@azure/cosmos';
```

---

## 2. Problemas de segurança

### 2.1 Logging de PII
O handler loga:
- attendantEmail
- comment

---

### 2.2 Sem limite de tamanho do comentário
Riscos de custo elevado no Cosmos e DoS.

---

### 2.3 Endpoint sem autenticação/autorização
Sem:
- API key
- JWT
- authLevel explícito

---

### 2.4 Cosmos client criado por request
Riscos de connection storm e socket exhaustion.

---

## 3. Bugs potenciais

### 3.1 Falta tratamento de erro do Cosmos
Sem try/catch, a função quebra.

---

### 3.2 Database/container hardcoded
Valores hardcoded:
- novatech
- feedbacks

---

### 3.3 Status code inadequado
Sempre retorna 200 OK.