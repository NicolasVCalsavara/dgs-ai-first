# Servidores MCP — NovaTech Assistant

> Documento de referência do setup MCP (Model Context Protocol) local e gratuito do projeto.
> Mapeia cada **necessidade do projeto** para um **reference server** oficial, descrevendo o que cada
> servidor expõe (Tools, Resources, Prompts), quem o consome e qual escopo recebe.
> Nenhum serviço pago ou externo é utilizado — tudo roda localmente.

---

## 1. Conceito

MCP (Model Context Protocol) padroniza como modelos de IA se conectam a ferramentas externas. Um MCP server expõe três tipos de capacidade:

- **Tools** — ações que o agente pode invocar (ler arquivo, escrever arquivo, consultar histórico Git, gravar memória).
- **Resources** — dados somente leitura acessíveis como URIs (`file:///...`), que o agente referencia sem precisar de uma chamada de tool.
- **Prompts** — templates reutilizáveis que o servidor oferece ao cliente.

Servers podem rodar localmente — não precisam ser serviços na nuvem. Neste projeto, quatro reference servers oficiais substituem integrações que normalmente seriam pagas ou externas (Confluence, Azure AI Search, etc.).

---

## 2. Visão geral do mapeamento

| Necessidade do projeto | Servidor | Tipo de acesso | Escopo |
|---|---|---|---|
| Código, specs e skills (ler/escrever) | `filesystem` | Tools + Resources | `src/`, `specs/`, `skills/`, `prompts/` |
| Documentação de negócio NovaTech (ler) | `filesystem` | Resources | `docs/novatech/` |
| Corpus de retrieval (ler) | `filesystem` | Resources | `data/retrieval-corpus/` |
| Histórico e branches do repositório | `git` | Tools | `.` (raiz do repo) |
| Memória persistente de decisões | `memory` | Tools | knowledge graph local |
| Validar o cliente MCP (teste/onboarding) | `everything` | Tools + Resources + Prompts | n/a |

---

## 3. `filesystem`

**Pacote:** `@modelcontextprotocol/server-filesystem`
**Substitui:** acesso direto ao código + Confluence (documentação) + Azure AI Search (corpus).

Atende três das cinco necessidades do projeto. É o servidor que mais trabalha: o agente de código lê e escreve em `src/`, `specs/`, `skills/` e `prompts/`, e lê em modo passivo a documentação de negócio e o corpus de retrieval.

### Tools expostas

| Tool | Função |
|---|---|
| `read_file` | Lê o conteúdo completo de um arquivo. |
| `read_multiple_files` | Lê vários arquivos numa única chamada (mais eficiente que chamadas sequenciais). |
| `write_file` | Cria ou sobrescreve um arquivo com novo conteúdo. |
| `edit_file` | Aplica edições cirúrgicas (estilo diff/patch) em arquivo existente. |
| `create_directory` | Cria diretório, incluindo subdiretórios intermediários. |
| `list_directory` | Lista arquivos e pastas dentro de um caminho. |
| `directory_tree` | Retorna a árvore completa de um diretório em formato estruturado. |
| `move_file` | Move ou renomeia arquivo/pasta. |
| `search_files` | Busca recursiva por nome de arquivo com suporte a glob. |
| `get_file_info` | Retorna metadados (tamanho, datas, permissões) sem ler o conteúdo. |
| `list_allowed_directories` | Lista as pastas autorizadas (os argumentos do `mcp.json`). |

### Resources expostos

Cada arquivo nas pastas autorizadas é exposto como resource com URI no formato `file:///caminho/absoluto/arquivo.ext`. O agente pode referenciar esses URIs diretamente em vez de chamar `read_file` — útil para leitura passiva da documentação e do corpus.

### Prompts

Nenhum. O `filesystem` não oferece templates de prompt.

### Escopo recebido

```
./src              (código — leitura/escrita)
./specs            (specs — leitura/escrita)
./skills           (skills — leitura/escrita)
./prompts          (system-prompt, changelog — leitura)
./docs/novatech    (documentação de negócio — leitura)
./data/retrieval-corpus  (corpus de chunks — leitura)
```

As pastas são listadas explicitamente por dois motivos: o servidor só enxerga o que recebe como argumento, e separar as pastas mantém `infra/`, `.github/` e `tests/` fora do alcance do agente de propósito. Operações fora dessas pastas são bloqueadas — o servidor rejeita path traversal (`../../`).

### Quem consome

Agente de código (geração de artefatos: endpoints, componentes React, testes de integração).

---

## 4. `git`

**Pacote:** `mcp-server-git` (executado via `uvx`)
**Substitui:** consultas manuais ao histórico do repositório.

Dá ao agente acesso ao histórico de versões — sem token, pois lê apenas o diretório `.git/` local.

### Tools expostas

| Tool | Função |
|---|---|
| `git_status` | Estado atual da árvore de trabalho (arquivos modificados, staged). |
| `git_log` | Histórico de commits. |
| `git_diff` | Diferenças entre commits, branches ou árvore de trabalho. |
| `git_diff_unstaged` / `git_diff_staged` | Diffs específicos do working tree e da staging area. |
| `git_show` | Conteúdo de um commit específico. |
| `git_blame` | Autoria linha a linha de um arquivo. |
| `git_branch` | Lista/gerencia branches. |
| `git_commit` | Cria um commit (escrita — usar com cautela em treinamento). |
| `git_add` | Adiciona arquivos à staging area. |
| `git_checkout` | Troca de branch. |

### Resources e Prompts

Nenhum. O `git` expõe apenas tools.

### Escopo recebido

```
--repository .   (raiz do repositório)
```

### Quem consome

Agente de revisão / análise (entender o que mudou, quem alterou determinada linha, comparar branches antes de gerar um artefato).

---

## 5. `memory`

**Pacote:** `@modelcontextprotocol/server-memory`
**Substitui:** anotações dispersas e perda de contexto entre sessões.

Mantém um **knowledge graph** persistente em arquivo local. É onde o projeto registra decisões arquiteturais (ADRs), a linguagem ubíqua e relações entre componentes — informação que sobrevive ao fim de uma sessão e é recuperada na próxima.

### Tools expostas

| Tool | Função |
|---|---|
| `create_entities` | Cria entidades no grafo (ex.: "ADR-0001", "chunker", "endpoint de query"). |
| `create_relations` | Cria relações entre entidades (ex.: "chunker → depende de → extractor"). |
| `add_observations` | Anexa observações/fatos a uma entidade existente. |
| `delete_entities` | Remove entidades. |
| `delete_relations` | Remove relações. |
| `delete_observations` | Remove observações específicas. |
| `read_graph` | Lê o grafo completo. |
| `search_nodes` | Busca nós por termo. |
| `open_nodes` | Abre nós específicos por nome. |

### Resources e Prompts

Nenhum. O `memory` expõe apenas tools; o estado é persistido num arquivo JSON local do knowledge graph.

### Escopo recebido

Nenhum argumento de pasta. O grafo é armazenado localmente (caminho padrão do servidor). Para fixar o local no repositório, defina a variável de ambiente `MEMORY_FILE_PATH`.

### Quem consome

Todos os agentes. Exemplos de uso no projeto:

- Registrar uma decisão: `create_entities` → "ADR-0002: regras de gerenciamento de contexto".
- Registrar linguagem ubíqua: entidade "chunk", "corpus de retrieval", "frete especial".
- Recuperar contexto numa nova sessão: `search_nodes("frete especial")` retorna a decisão e suas relações.

---

## 6. `everything`

**Pacote:** `@modelcontextprotocol/server-everything`
**Finalidade:** servidor de referência/teste — não cobre necessidade de negócio direta.

É o "hello world" do protocolo. Expõe os **três** tipos de capacidade (Tools, Resources e Prompts) justamente para exercitar todas as features de um cliente MCP. Se ele responder, o cliente está corretamente configurado.

### O que expõe

- **Tools** de demonstração (echo, soma, operações de exemplo que retornam valores previsíveis).
- **Resources** de teste (recursos sintéticos com URIs de exemplo).
- **Prompts** de exemplo (templates que o cliente pode listar e renderizar).

### Escopo recebido

Nenhum. Não acessa o sistema de arquivos do projeto.

### Quem consome

Desenvolvedor / processo de onboarding — para validar o setup MCP antes de confiar nos servidores reais.

---

## 7. Configuração (`mcp.json`) — Windows 11

Entradas baseadas em `npx` são embrulhadas com `cmd /c` (no Windows, `npx` é um script `.cmd` e não resolve corretamente quando chamado diretamente pelo cliente MCP). A entrada `git`, baseada em `uvx`, permanece inalterada.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "cmd",
      "args": [
        "/c", "npx", "-y", "@modelcontextprotocol/server-filesystem",
        "./src", "./specs", "./skills",
        "./docs/novatech", "./data/retrieval-corpus", "./prompts"
      ]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "."]
    },
    "memory": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-memory"]
    },
    "everything": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-everything"]
    }
  }
}
```

---

## 8. Resumo de exposição por servidor

| Servidor | Tools | Resources | Prompts | Escreve? |
|---|---|---|---|---|
| `filesystem` | ✓ (11) | ✓ (arquivos como URIs) | — | Sim (em `src/`, `specs/`, `skills/`) |
| `git` | ✓ (10) | — | — | Sim (`commit`, `add` — opcionais) |
| `memory` | ✓ (9) | — | — | Sim (grafo local) |
| `everything` | ✓ | ✓ | ✓ | Não (apenas teste) |
