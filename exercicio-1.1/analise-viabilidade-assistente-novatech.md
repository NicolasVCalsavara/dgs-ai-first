# Análise de Viabilidade Técnica — Assistente de IA para Atendimento

**Cliente:** NovaTech (logística, ~1.200 funcionários)
**Executor:** DB1
**Escopo do documento:** Viabilidade técnica de um assistente de IA (RAG) que responde perguntas dos atendentes em linguagem natural, fundamentado na documentação oficial, com citação de fonte. Integração ao ambiente Microsoft (Teams + SharePoint).
**Foco analítico solicitado pelo tech lead:** características da documentação da NovaTech e impacto do gerenciamento de contexto na arquitetura.

---

## 1. Veredito de viabilidade

Tecnicamente **viável**, com o stack Microsoft/Azure que a NovaTech já licencia ou está disposta a provisionar. A meta da diretoria (reduzir a busca de 12 para menos de 2 minutos) é **alcançável para os ~60% de chamados que consultam documentação** — cerca de 190 chamados/dia — desde que os desafios de tabelas complexas, OCR e versionamento sejam tratados de forma específica, e não com um RAG genérico de prateleira.

A janela de 3 meses (discovery + desenvolvimento + go-live) é **apertada, porém factível para um MVP de escopo controlado**. Recomenda-se fatiar o go-live começando pelos domínios que concentram valor e risco: regras de frete, SLA por cliente e política de devolução.

O maior risco do projeto **não é técnico, é de governança** (ver Seção 7): a documentação se contradiz entre versões e é mantida por três áreas sem processo unificado. RAG propaga contradições fielmente; ele mitiga, mas não resolve a causa raiz.

---

## 2. Análise das fontes de documentação

A base vive em três fontes heterogêneas. Cada tipo de conteúdo impõe um desafio distinto ao pipeline de RAG.

### 2.1. PDFs com tabelas complexas (15+ colunas)

**Desafio.** A extração ingênua de texto *lineariza* a tabela: o relacionamento linha–coluna desaparece. Uma tabela de frete vira uma sequência de números na qual o LLM não consegue mapear, por exemplo, "R$ 47,20" à célula correta (região × faixa de peso × tipo de cliente). O chunking de tamanho fixo agrava o problema ao cortar a tabela no meio de uma linha ou separar o cabeçalho dos dados.

**Impacto na qualidade.** É o pior modo de falha: o assistente responde um valor de frete **errado, com confiança e sem sinal de incerteza**. Como frete e SLA são justamente as perguntas de maior consequência, esse risco é inaceitável sem tratamento.

**Estratégia.**
- Extração *layout-aware* com **Azure AI Document Intelligence** (modelo Layout), que preserva a estrutura tabular.
- Serializar cada tabela em Markdown/HTML mantendo os cabeçalhos.
- Tratar a tabela como **chunk atômico** (nunca dividir). Em tabelas muito grandes, fazer chunk por linha repetindo o cabeçalho em cada chunk.
- **Ponto contraintuitivo:** regras de cálculo de frete provavelmente *não deveriam passar por RAG*. Cálculo é lógica determinística — o ideal é expor a tabela de frete como dado estruturado e o assistente executar um *lookup* via tool/function calling, em vez de recuperar texto e confiar que o LLM some corretamente.

### 2.2. PDFs escaneados (OCR necessário)

**Desafio.** Sem camada de texto, dependemos de OCR. O erro de OCR em números é **silencioso**: um "8" lido como "3" num prazo de SLA não gera erro de sistema, gera resposta errada. O risco se concentra justamente em tabelas numéricas escaneadas.

**Impacto na qualidade.** *Garbage in, garbage out* — e como o erro é silencioso, ele não é detectado pelo pipeline, só pelo cliente final.

**Estratégia.**
- OCR via Document Intelligence com *confidence scores* e *threshold* na ingestão.
- Sinalizar para revisão humana os documentos de baixa confiança.
- Para documentos críticos (frete, segurança de carga), avaliar a migração para texto nativo em vez de confiar no OCR — é o investimento que mais reduz risco.
- Aplicar um *quality gate* antes de o conteúdo entrar no índice.

### 2.3. Wiki Confluence (links internos + macros customizadas)

**Desafio.** Dois problemas distintos. (a) Links internos: o contexto de uma página vive *fora* dela — um chunk que diz "ver política de devolução em [link]" é inútil se o conteúdo do link não está no contexto. (b) Macros customizadas: renderizam conteúdo dinamicamente; o *export* bruto (storage format) pode não conter o que o usuário enxerga na tela.

**Impacto na qualidade.** Respostas incompletas que perdem informação referenciada por link, ou que omitem conteúdo gerado por macro.

**Estratégia.**
- Ingerir via **API REST do Confluence pegando o formato renderizado** (não o raw), de modo que as macros já venham resolvidas.
- Preservar a hierarquia de páginas e o grafo de links como **metadados** do chunk, viabilizando recuperação multi-hop ou ao menos a expansão de referências críticas.
- Inlinar os *includes* importantes durante a ingestão.

### 2.4. Planilhas com fórmulas interdependentes

**Desafio.** A resposta nunca é a fórmula — é o **valor calculado**. Serializar o texto da fórmula (`=VLOOKUP(...)`) é inútil para recuperação; serializar só os valores perde a lógica e fica obsoleto no mês seguinte. A interdependência significa que o sentido de uma célula depende de outras. Como contêm SLA e frete e são atualizadas mensalmente, são **alto valor e alto risco de obsolescência**.

**Impacto na qualidade.** Snapshot estático envelhece e passa a contradizer a fonte viva, reintroduzindo o problema de inconsistência que o projeto busca eliminar.

**Estratégia.**
- A mesma das tabelas de frete: **não tratar como texto de RAG**.
- Computar os valores na ingestão e expor a planilha como dado estruturado (banco ou índice tabular) consumido via tool/function.
- Reindexar acoplado ao ciclo mensal de atualização.
- Se mantidas como texto, no mínimo exportar valores calculados — nunca fórmulas.

---

## 3. Dimensionamento da base (tokens)

**Regra de conversão.** "0,75 palavras por token" significa 1 token ≈ 0,75 palavra (forma canônica: 100 tokens ≈ 75 palavras). Logo a conversão correta é **tokens = palavras ÷ 0,75** (≈ palavras × 1,33). Multiplicar por 0,75 inverteria a regra e subestimaria a base em ~44%.

A estimativa separa o que é **explícito** no enunciado do que **exige premissa declarada**.

### 3.1. Componente explícito (sem premissa)

| Fonte | Cálculo | Palavras | Tokens (÷ 0,75) |
|---|---|---|---|
| Wiki | 400 × 1.500 | 600.000 | **800.000 (~0,80M)** |

A wiki é o único componente totalmente determinado pelo enunciado. É o número-âncora.

### 3.2. Componentes que exigem premissa

**PDFs** — o enunciado dá 800 × 10 = 8.000 páginas, mas **não informa palavras por página**. Como são páginas com tabelas e imagens (que deslocam texto), adoto ~500 palavras/página como estimativa central de página corporativa em espaço simples, com a banda de sensibilidade:

| Premissa (palavras/pág.) | Palavras | Tokens (÷ 0,75) |
|---|---|---|
| 400 (conservador) | 3.200.000 | ~4,27M |
| **500 (central)** | **4.000.000** | **~5,33M** |
| 650 (denso) | 5.200.000 | ~6,93M |

**Planilhas** — componente mais incerto: 50 planilhas sem dimensão informada. Serializadas para texto, variam de tabelas de lookup pequenas a tabelas de referência grandes:

| Premissa (palavras/planilha) | Tokens (÷ 0,75) |
|---|---|
| 1.000 | ~0,07M |
| **3.000 (central)** | **~0,20M** |
| 10.000 | ~0,67M |

### 3.3. Consolidação

| Fonte | Base | Tokens (cenário central) |
|---|---|---|
| PDFs | premissa | ~5,33M |
| Wiki | **explícito** | ~0,80M |
| Planilhas | premissa | ~0,20M |
| **Total central** | | **~6,3M tokens** |

- **Piso rigorosamente explícito (só wiki):** ~0,8M tokens.
- **Faixa realista com as premissas:** ~5,1M a ~8,4M tokens.
- Os PDFs dominam (~84% do total), mas dependem da premissa de densidade — **recomenda-se amostrar 10–15 documentos reais no discovery** para fechar o número.

**Implicação:** em qualquer ponto da faixa, a base é **~40 a 65× a janela de 128K** do GPT-4o. Isso confirma que recuperação seletiva (RAG) é a abordagem correta e que não existe cenário em que despejar a base toda no contexto faça sentido. A conclusão de arquitetura é **robusta à incerteza dos números**.

---

## 4. Orçamento de contexto

Considerando GPT-4o (janela de 128K) e system prompt + instruções consumindo ~2K tokens:

- **Conta direta:** 128.000 − 2.000 = 126.000 tokens → a 500 tokens/chunk, cabem **~252 chunks**.
- **Conta realista:** descontando reservas para a saída (resposta fundamentada, ~1–2K), histórico de conversa (cresce ao longo do chamado) e a query, o espaço útil cai para ~110–120K → ~**220 chunks**.

**Mas esse número é uma armadilha.** Encher o contexto com 200+ chunks **degrada** a qualidade (ver Seção 5 — *lost in the middle*), além de elevar custo e latência por query.

**Leitura correta:** o orçamento de contexto **não é o gargalo** — o gargalo é a *relevância* da recuperação. Com 252 vagas teóricas e necessidade de usar apenas ~5–10, o esforço de engenharia se desloca de "como faço caber" para "como garanto que os chunks certos sejam selecionados e bem posicionados". Investir em *reranking* e recuperação híbrida rende muito mais do que aumentar o número de chunks entregues ao modelo.

---

## 5. Estratégia de chunking e retrieval

### 5.1. Justificativa pelo tipo de pergunta

As perguntas dos atendentes são majoritariamente **factuais e pontuais**: "qual o prazo de SLA do cliente X", "como processar uma reclamação de avaria", "qual a regra de frete para a região Sul". A resposta vive em *um trecho específico e bem delimitado* da documentação — não espalhada por dezenas de páginas. Isso favorece chunks coesos e semanticamente completos em vez de chunks grandes e genéricos.

### 5.2. Recomendações

- **Chunking estrutural, não de tamanho fixo cego.** Quebrar respeitando a estrutura do documento (por seção/heading), mantendo passos de procedimento juntos e **nunca cortando tabelas**. Tamanho-alvo de ~500–800 tokens, com *overlap* de ~10–15% para preservar contexto na fronteira.
- **Metadados ricos por chunk:** fonte, área dona (Operações/Compliance/Comercial), data e **versão** — críticos para o problema de contradição (Seção 7).
- **Recuperação híbrida (keyword + vetorial):** perguntas de SLA e frete contêm termos exatos (nomes de cliente, códigos, regiões) que a busca puramente semântica erra. O **Azure AI Search** oferece isso nativamente.
- **Recuperar amplo, entregar estreito:** buscar ~30–40 candidatos → reordenar com *reranker* (semantic ranker do Azure AI Search ou Cohere Rerank) → entregar ao LLM apenas os **top 5–10**.

### 5.3. *Lost in the middle*

A informação posicionada no **meio** de um contexto longo é efetivamente ignorada pelo modelo. Implicações práticas:

1. **Não encher o contexto** — 10 chunks ótimos superam 100 medianos.
2. **Posicionar deliberadamente** — colocar os chunks de maior score no *início* e no *fim* do bloco de contexto, deixando os de menor confiança no meio.
3. **Gerenciar o histórico** — truncar/resumir turnos antigos da conversa para que não empurrem os chunks recuperados para a zona morta central nem consumam orçamento de atenção à toa.

---

## 6. Arquitetura recomendada (mapa para o stack Microsoft)

| Camada | Componente | Papel |
|---|---|---|
| Ingestão / parsing | Azure AI Document Intelligence | Extração layout-aware de tabelas + OCR de escaneados |
| Ingestão / wiki | Confluence REST API (formato renderizado) | Resolver macros e preservar grafo de links |
| Dados estruturados | Índice tabular / banco + function calling | Frete e planilhas como lookup determinístico |
| Índice de busca | Azure AI Search (híbrido + semantic ranker) | Recuperação + reranking |
| Geração | Azure OpenAI (GPT-4o) | Resposta fundamentada com citação de fonte |
| Front-end | Teams (bot ou Copilot Studio) | Interface no fluxo de trabalho do atendente |

Observação de design coerente com o foco em gerenciamento de contexto: **nem tudo deve ser RAG**. Conteúdo determinístico (frete, SLA tabular) deve ser servido por tool/function calling; texto procedimental e normativo é o que efetivamente passa pelo pipeline de recuperação.

---

## 7. Riscos e premissas

**R1 — Contradição entre documentos (risco principal, de governança).** RAG não resolve a contradição entre versões — ele a propaga fielmente. Hoje a equipe resolve "perguntando para quem sabe"; se as fontes se contradizem, o assistente recuperará as duas versões e ou escolherá arbitrariamente ou apresentará respostas inconsistentes — o mesmo problema, agora automatizado e com aparência de autoridade.
*Mitigação:* priorizar a versão mais recente via metadado de data; sempre citar fonte + data; sinalizar conflitos detectados ao atendente.
*Causa raiz:* ausência de processo unificado de revisão entre Operações, Compliance e Comercial. **É uma lacuna de governança, não de engenharia.** Deve ser registrada no discovery como pré-requisito ou risco assumido — caso contrário, a diretoria cobrará da DB1 uma consistência que a fonte não possui.

**R2 — Qualidade da extração de tabelas.** Falha aqui produz erros silenciosos em frete/SLA. Mitigação: Document Intelligence + tabelas como chunks atômicos + roteamento de cálculo para lógica determinística.

**R3 — Erros silenciosos de OCR.** Mitigação: thresholds de confiança, revisão humana de baixa confiança, migração de documentos críticos para texto nativo.

**R4 — Obsolescência das planilhas.** Mitigação: reindexação acoplada ao ciclo mensal de atualização.

**R5 — Prazo de 3 meses.** Mitigação: MVP de escopo controlado (frete + SLA + devolução primeiro).

**Premissa a validar (P1):** densidade dos PDFs (palavras/página). O total da base depende dela e foi estimado, não medido. Validar amostrando 10–15 documentos reais no discovery.

---

## 8. Próximos passos sugeridos

1. **Discovery dirigido:** amostrar PDFs reais (validar P1), mapear o grau de contradição entre versões (dimensionar R1) e inventariar quais planilhas/tabelas devem virar dados estruturados.
2. **Acordar com a NovaTech** o tratamento da lacuna de governança (R1) antes do desenvolvimento.
3. **Definir o recorte do MVP** (frete + SLA + devolução) e o pipeline de atualização mensal.
4. **Prova de conceito de extração** nas tabelas de frete mais complexas, por ser o ponto de maior risco técnico.
