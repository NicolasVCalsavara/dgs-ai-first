# Catálogo de Skills — NovaTech Assistant

Companheiro de `skills-tree.md`. Uma linha por skill, com frase-ativação, autoria, consumo e frequência.

**Convenção desta tabela**
- **Cria** = papel que escreve e mantém o arquivo `.md` da skill.
- **Consome** = papel humano + agente que invoca a skill ao gerar um artefato.
- **Frase-ativação** = condição em linguagem natural que faz um agente reconhecer que a skill se aplica.

**Papéis:** PM (Product Specialist) · TL (Tech Lead) · DevSr (Dev Sênior) · DevB (Dev Backend) · DevF (Dev Frontend)
**Agentes** (papéis que um agente assume; pode ser o mesmo modelo por baixo):
- **Ag-Impl** — agente de implementação (Copilot/agent mode no VS Code): gera código e testes.
- **Ag-Review** — agente de revisão: confere o output contra as convenções.
- **Ag-Spec** — agente de spec/planejamento: apoia requirements/plan/tasks.
- **Ag-Docs** — agente de documentação: gera ADR/README.

**Escala de frequência**
- **Muito alta** — referenciada em quase toda geração de código.
- **Alta** — usada em cada artefato de uma categoria recorrente.
- **Média** — usada várias vezes no projeto, não a cada artefato.
- **Baixa** — uso pontual.

---

## Foundation

| Skill | Frase-ativação | Cria | Consome (papel + agentes) | Frequência |
|---|---|---|---|---|
| `typescript-conventions` | "Ao escrever ou revisar qualquer código TypeScript do projeto." | TL / DevSr | Todos os Devs · Ag-Impl, Ag-Review | Muito alta |
| `error-handling` | "Ao lançar, capturar ou converter um erro em resposta/efeito — definir status, mensagem PT-BR e evitar vazamento de segredo." | TL | DevB, DevF · Ag-Impl, Ag-Review | Muito alta |
| `logging-observability` | "Ao adicionar logs, correlação de request ou observabilidade a um serviço/endpoint." | TL / DevSr | DevB · Ag-Impl, Ag-Review | Alta |
| `env-config` | "Ao ler configuração de ambiente ou introduzir uma nova variável obrigatória." | TL | DevB · Ag-Impl, Ag-Review | Média |
| `testing-conventions` | "Ao escrever ou revisar qualquer teste — garantir asserções que sempre executam (sem false-green)." | TL / DevSr | Todos os Devs · Ag-Impl, Ag-Review | Muito alta |
| `project-structure` | "Ao decidir onde um novo arquivo/módulo deve morar ou como nomeá-lo." | TL | Todos os Devs · Ag-Impl, Ag-Spec | Alta |

---

## Domain

| Skill | Frase-ativação | Cria | Consome (papel + agentes) | Frequência |
|---|---|---|---|---|
| `azure-functions-endpoint` | "Ao criar ou alterar um HTTP trigger de Azure Functions (handler / validator / response-builder)." | TL / DevSr | DevB · Ag-Impl, Ag-Review | Alta |
| `rag-query-pattern` | "Ao implementar o fluxo recuperar+gerar: embed → search → montar prompt → completion → atribuir fonte." | TL / DevSr | DevB · Ag-Impl | Alta |
| `azure-ai-search-integration` | "Ao integrar com Azure AI Search: embeddings, busca top-k, retry/backoff." | DevSr / TL | DevB · Ag-Impl | Média |
| `testing-patterns` | "Ao escolher o tipo de teste (unit/integration/e2e), montar fixtures ou mockar Azure." | DevSr / TL | DevB, DevF · Ag-Impl, Ag-Review | Alta |
| `react-components` | "Ao criar ou organizar um componente do painel web React." | DevF / TL | DevF · Ag-Impl, Ag-Review | Alta |
| `technical-documentation` | "Ao escrever um ADR ou o README de um módulo." | TL | TL, DevB, DevF · Ag-Docs | Média |
| `sdd-spec-authoring` | "Ao redigir requirements/plan/tasks ou decidir o grão de uma task (fatia vertical)." | TL / PM | PM, TL, Dev · Ag-Spec | Média |

---

## Artifact

| Skill | Frase-ativação | Cria | Consome (papel + agentes) | Frequência |
|---|---|---|---|---|
| `create-rag-endpoint` | "Quando o pedido for criar/adicionar um novo endpoint RAG (ex.: query, busca semântica)." | TL / DevSr | DevB · Ag-Impl | Alta |
| `create-integration-test` | "Quando o pedido for gerar a suíte de integração de um endpoint." | DevSr | DevB · Ag-Impl | Alta |
| `create-react-card` | "Quando o pedido for criar um card de resposta no painel." | DevF | DevF · Ag-Impl | Média |
| `create-feedback-form` | "Quando o pedido for criar um formulário de feedback no painel." | DevF | DevF · Ag-Impl | Baixa |
| `create-adr` | "Quando o pedido for registrar uma decisão de arquitetura." | TL | TL, DevSr · Ag-Docs | Média |
| `create-module-readme` | "Quando o pedido for gerar ou atualizar o README de um módulo." | TL / Dev | Dev · Ag-Docs | Baixa |
| `create-spec` | "Quando o pedido for iniciar a spec SDD de um módulo (requirements / plan / tasks)." | PM / TL | PM (req), TL (plan), Dev (tasks) · Ag-Spec | Média |

---

## Leitura cruzada — padrões que valem notar

- **Quem mais consome são os agentes, não as pessoas.** Toda Foundation e Domain é lida pelo Ag-Impl a cada geração; o humano entra como autor e revisor. Por isso a frase-ativação importa tanto: é ela que faz o agente puxar a skill certa sem o dev pedir explicitamente.
- **Autoria concentra no TL.** O Tech Lead cria/mantém a maioria das Foundation e Domain (são contrato técnico). DevF é dono das skills de painel; PM co-cria só as de spec. Isso espelha quem tem autoridade sobre cada convenção.
- **Frequência ≠ esforço de manutenção.** `error-handling` e `testing-conventions` são "Muito alta" em uso mas mudam raramente — alto retorno por edição. As receitas Artifact mudam mais (evoluem com o padrão), mas cada uma é invocada com frequência menor.
- **As "Muito alta" são as candidatas a virar contexto sempre-ligado do agente** (regras de projeto / instruções persistentes), enquanto as Artifact fazem mais sentido como skills sob demanda, invocadas pela frase-ativação.
