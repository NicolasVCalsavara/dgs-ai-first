• Gerado mcp_server_mapping_novatech.svg

• Gerado MCP-SERVERS-NOVATECH.md

• Discutido controle de acesso. Resultado da conversa:

Essa é a parte mais importante — e tem uma armadilha técnica. O servidor `filesystem` de referência, quando recebe pastas como argumentos posicionais, concede **leitura E escrita** a todas elas. Ou seja, listar `docs/novatech` junto de `src` **não** torna a documentação read-only. Antes de te entregar algo que parece least privilege mas não é, deixa eu verificar exatamente o que a versão atual do servidor suporta.Confirmado — e isso muda o desenho. Puxei o README da versão atual (`2026.1.14`) do servidor `filesystem`. Pontos decisivos:

1. **Não existe flag de read-only.** Toda pasta passada como argumento é tratada como **read/write**. O próprio `list_allowed_directories` descreve as pastas como "directories this server can read/write from". Os `readOnlyHint` que o servidor publica são apenas *dicas* para o cliente — as tools de escrita (`write_file`, `edit_file`, `move_file`) continuam existindo e funcionando em qualquer pasta permitida.
2. **O controle de acesso real é o conjunto de pastas permitidas.** O servidor recusa qualquer operação fora delas. Então o que de fato limita privilégio é *o que você não passa*.

Conclusão: listar `docs/novatech` junto de `src` num único server **não** as torna read-only — pelo contrário, dá escrita a elas. Least privilege concreto aqui exige duas coisas: separar em instâncias e fechar o buraco residual com permissão de SO.

## Desenho revisado

Duas instâncias do `filesystem`:

- **`filesystem-workspace`** — read/write, recebe **só** `src/`, `specs/`, `skills/`. Como `docs/` e `data/` não estão na lista de pastas permitidas, as tools de escrita desta instância **fisicamente não conseguem** tocá-las (o server rejeita o path). Isso é enforcement, não convenção.
- **`filesystem-sources`** — serve `docs/novatech/`, `data/retrieval-corpus/` e `prompts/`. Como o server não tem modo read-only, o read-only é imposto por **ACL do Windows** (negar escrita), mostrado abaixo.## Enforcement do read-only no Windows 11

A separação por si só não impede que o agente escreva via `filesystem-sources`. Negue escrita nas duas pastas com `icacls` (execute na raiz do repo, PowerShell ou cmd):

```bat
icacls "docs\novatech"          /deny "%USERNAME%:(WD,AD,WA,WEA,DC,DE)" /T
icacls "data\retrieval-corpus"  /deny "%USERNAME%:(WD,AD,WA,WEA,DC,DE)" /T
```

Isso adiciona um ACE de negação de escrita (criar arquivo/pasta, anexar, alterar atributos, deletar) ao usuário que roda o cliente MCP — então `write_file`/`edit_file` falham com acesso negado, mesmo o caminho estando na allowlist. Para reverter: troque `/deny` por `/remove:d`. (`prompts/` deixei sem ACL de negação: se você quiser que ele também seja imutável, aplique o mesmo comando; se o agente precisar versionar o `prompt-changelog.md`, mantenha-o gravável.)

## Por que cada escopo é o mínimo suficiente

**`src/`, `specs/`, `skills/` (read-write).** São os únicos lugares onde o agente *produz* artefatos: código nas funções/pipeline/bot, specs no fluxo spec-driven (plan/requirements/tasks) e skills. Sem escrita aqui, o agente não cumpre sua função; com escrita só aqui, o raio de impacto de uma alucinação ou comando errado fica contido a artefatos versionados e recuperáveis via Git.

**`docs/novatech/` (read-only).** É a fonte de verdade de negócio (substitui o Confluence). O agente precisa *consultar* política de devolução, SLA e procedimentos de frete — nunca reescrevê-los. Escrita aqui seria adulteração silenciosa de regra de negócio, o pior caso de RAG.

**`data/retrieval-corpus/` (read-only).** É o corpus de "recuperação" (substitui o Azure AI Search). O agente recupera chunks lendo; escrever no corpus envenenaria a base de recuperação para todas as consultas futuras.

**`prompts/` (read, em instância separada).** Contém o `system-prompt.md` (os próprios guardrails do agente) e `golden-queries.json` (conjunto de avaliação). Manter fora da instância gravável impede que o agente reescreva as próprias instruções ou o gabarito dos testes — um ponto de least privilege que é também de segurança.

**Fora de qualquer instância: `infra/`, `.github/`, `tests/`, raiz.** Não passar essas pastas é a forma mais forte de negar acesso. Bicep de infraestrutura e workflows de CI/CD não têm relação com geração de artefatos de RAG; deixá-los inacessíveis elimina a possibilidade de o agente alterar deploy ou pipeline.

Uma observação honesta para fechar: o servidor `git` desta config ainda expõe `git_commit`/`git_add` (escrita), e ele também não tem modo read-only nativo. Se o exercício for estritamente de leitura de histórico, vale combinar com o time se o agente deve poder commitar — caso contrário, isso fica como um privilégio a mais do que o mínimo.

• **OBS.:** dentro da realidade do projeto em que estou, não tenho como rodar `icacls` por falta de privilégios suficientes.