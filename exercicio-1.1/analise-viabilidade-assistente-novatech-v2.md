# Análise de Viabilidade Técnica — Assistente de IA para Atendimento

**Cliente:** NovaTech (logística, ~1.200 funcionários)
**Executor:** DB1
**Escopo do documento:** Viabilidade técnica de um assistente de IA (RAG) que responde perguntas dos atendentes em linguagem natural, fundamentado na documentação oficial, com citação de fonte. Integração ao ambiente Microsoft (Teams + SharePoint).
**Foco analítico solicitado pelo tech lead:** características da documentação da NovaTech e impacto do gerenciamento de contexto na arquitetura.

> **Histórico de revisão — v2.** Esta revisão incorpora itens ausentes na v1: metodologia de avaliação e critérios de aceite (Seção 7), segurança/permissões e LGPD (Seção 8), comportamento de abstenção (Seção 6), custo (Seção 10) e cronograma com dependências do cliente (Seção 11). Foram ajustados: o veredito de prazo (Seção 1, agora mais conservador), a ligação entre o KPI de tempo e a meta de acurácia (Seções 1 e 7), a tokenização do português (Seção 3), a reconciliação entre estimativa de tokens e arquitetura (Seções 3 e 9), e o esforço de ETL de dados estruturados (Seções 2 e 11). Riscos R6–R12 acrescentados (Seção 12).

---

## 1. Veredito de viabilidade

Tecnicamente **viável**, com o stack Microsoft/Azure que a NovaTech já licencia ou está disposta a provisionar. A meta da diretoria (reduzir a busca de 12 para menos de 2 minutos) é **alcançável para os ~60% de chamados que consultam documentação** — cerca de 190 chamados/dia — **condicionada a uma ressalva que a v1 não tornava explícita: o ganho de tempo não depende da latência do sistema (que será de segundos), e sim de a resposta estar correta e de o atendente confiar nela sem reconferir.** Se a acurácia for baixa, os atendentes re-verificarão tudo e a economia evapora. Logo, a meta de tempo só se sustenta acoplada a uma **meta de acurácia formal** (ver Seção 7). Tratamos as duas como uma só meta, não como metas independentes.

A viabilidade pressupõe ainda que os desafios de tabelas complexas, OCR e versionamento sejam tratados de forma específica, e não com um RAG genérico de prateleira.

A janela de 3 meses (discovery + desenvolvimento + go-live) é **apertada de verdade — não "apertada, porém confortável".** A v1 subestimava dois fatores: (a) o MVP escolhido concentra justamente os problemas técnicos mais difíceis (não é uma fatia "leve"); e (b) parte crítica do cronograma depende de ações da NovaTech que a DB1 não controla (acordo de governança, migração de documentos para texto nativo). O detalhamento e as mitigações estão na Seção 11. Mantém-se o fatiamento começando pelos domínios que concentram valor e risco: regras de frete, SLA por cliente e política de devolução — com a ciência de que essa fatia é o núcleo difícil, escolhido por valor, não por facilidade.

O maior risco do projeto **não é técnico, é de governança** (ver R1, Seção 12): a documentação se contradiz entre versões e é mantida por três áreas sem processo unificado. RAG propaga contradições fielmente; ele mitiga, mas não resolve a causa raiz.

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
- **Ressalva de esforço (nova na v2):** mover frete para dado estruturado é arquiteturalmente correto, mas **não é "de graça"**. Transformar 800 PDFs heterogêneos (parte escaneados, com risco de OCR) numa fonte estruturada confiável, e mantê-la, é um projeto de engenharia de dados por si só, não um detalhe de implementação. O custo desse ETL está dimensionado na Seção 11.

### 2.2. PDFs escaneados (OCR necessário)

**Desafio.** Sem camada de texto, dependemos de OCR. O erro de OCR em números é **silencioso**: um "8" lido como "3" num prazo de SLA não gera erro de sistema, gera resposta errada. O risco se concentra justamente em tabelas numéricas escaneadas.

**Impacto na qualidade.** *Garbage in, garbage out* — e como o erro é silencioso, ele não é detectado pelo pipeline, só pelo cliente final.

**Estratégia.**
- OCR via Document Intelligence com *confidence scores* e *threshold* na ingestão.
- Sinalizar para revisão humana os documentos de baixa confiança.
- Para documentos críticos (frete, segurança de carga), avaliar a migração para texto nativo em vez de confiar no OCR — é o investimento que mais reduz risco. **Atenção (v2):** isso é trabalho manual de quem conhece os valores corretos, do lado da NovaTech — é uma dependência de cronograma, não algo que a DB1 entrega sozinha (ver R10, Seção 12).
- Aplicar um *quality gate* antes de o conteúdo entrar no índice.

### 2.3. Wiki Confluence (links internos + macros customizadas)

**Desafio.** Dois problemas distintos. (a) Links internos: o contexto de uma página vive *fora* dela — um chunk que diz "ver política de devolução em [link]" é inútil se o conteúdo do link não está no contexto. (b) Macros customizadas: renderizam conteúdo dinamicamente; o *export* bruto (storage format) pode não conter o que o usuário enxerga na tela.

**Impacto na qualidade.** Respostas incompletas que perdem informação referenciada por link, ou que omitem conteúdo gerado por macro.

**Estratégia.**
- Ingerir via **API REST do Confluence pegando o formato renderizado** (não o raw), de modo que as macros já venham resolvidas.
- Preservar a hierarquia de páginas e o grafo de links como **metadados** do chunk, viabilizando a expansão de referências críticas durante a recuperação.
- Inlinar os *includes* importantes durante a ingestão.
- **Nota de honestidade técnica (v2):** recuperação *multi-hop* de verdade (seguir cadeias de links em tempo de query) é genuinamente difícil e não deve ser prometida para o MVP. A abordagem realista é **inlinar referências críticas na ingestão** (resolver o link uma vez, antes do índice) em vez de tentar segui-las em runtime. Multi-hop fica como evolução pós-MVP, não como requisito.

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

**Ressalva de idioma (nova na v2).** A razão 0,75 palavra/token é uma heurística do **inglês**. O português tokeniza pior (acentuação, palavras mais longas, menor representação no tokenizer), então o número real tende a ser **~10–25% maior por palavra**. Isso **não** derruba a conclusão de que RAG é necessário (essa é robusta — ver fim da seção), mas afeta o custo de embedding e a contagem de tokens por query. **Recomendação concreta:** ao amostrar os 10–15 documentos reais no discovery (premissa P1), **meça tokens diretamente com o tokenizer do modelo (o200k_base para GPT-4o), não palavras** — os arquivos já estarão em mãos, e isso elimina de uma vez a incerteza da densidade e a do idioma.

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
- **Faixa realista com as premissas:** ~5,1M a ~8,4M tokens (e provavelmente mais ~10–25% por causa do português — ver ressalva de idioma acima).
- Os PDFs dominam (~84% do total), mas dependem da premissa de densidade — **recomenda-se amostrar 10–15 documentos reais no discovery** para fechar o número, medindo tokens diretamente.

**Reconciliação com a arquitetura (nova na v2).** Este total é o corpus **bruto**. Mas as decisões da Seção 2 e da Seção 9 retiram frete e planilhas do **índice de texto** (viram dado estruturado servido por function calling). Logo, o **corpus efetivo de RAG** é menor que os ~6,3M e mais **procedimental/normativo** do que o número bruto sugere — o que reforça, e não enfraquece, a estratégia de chunking da Seção 5. O número de ~6,3M é correto para dimensionar embedding/ingestão totais; não é o tamanho do índice de recuperação textual.

**Implicação:** em qualquer ponto da faixa, a base é **~40 a 65× a janela de 128K** do GPT-4o. Isso confirma que recuperação seletiva (RAG) é a abordagem correta e que não existe cenário em que despejar a base toda no contexto faça sentido. A conclusão de arquitetura é **robusta à incerteza dos números** (e ao ajuste do português, que só aumenta o múltiplo).

---

## 4. Orçamento de contexto

Considerando GPT-4o (janela de 128K) e system prompt + instruções consumindo ~2K tokens:

- **Conta direta:** 128.000 − 2.000 = 126.000 tokens → a 500 tokens/chunk, cabem **~252 chunks** (a ~800 tokens/chunk — topo da faixa da Seção 5 — cairia para ~157; a ordem de grandeza não muda a conclusão).
- **Conta realista:** descontando reservas para a saída (resposta fundamentada, ~1–2K), histórico de conversa (cresce ao longo do chamado) e a query, o espaço útil cai para ~110–120K → ~**220 chunks**.

**Mas esse número é uma armadilha.** Encher o contexto com 200+ chunks **degrada** a qualidade (ver Seção 5 — *lost in the middle*), além de elevar custo e latência por query.

**Leitura correta:** o orçamento de contexto **não é o gargalo** — o gargalo é a *relevância* da recuperação. Com 252 vagas teóricas e necessidade de usar apenas ~5–10, o esforço de engenharia se desloca de "como faço caber" para "como garanto que os chunks certos sejam selecionados e bem posicionados". Investir em *reranking* e recuperação híbrida rende muito mais do que aumentar o número de chunks entregues ao modelo.

---

## 5. Estratégia de chunking e retrieval

### 5.1. Justificativa pelo tipo de pergunta

As perguntas dos atendentes são majoritariamente **factuais e pontuais**: "qual o prazo de SLA do cliente X", "como processar uma reclamação de avaria", "qual a regra de frete para a região Sul". A resposta vive em *um trecho específico e bem delimitado* da documentação — não espalhada por dezenas de páginas. Isso favorece chunks coesos e semanticamente completos em vez de chunks grandes e genéricos.

### 5.2. Recomendações

- **Chunking estrutural, não de tamanho fixo cego.** Quebrar respeitando a estrutura do documento (por seção/heading), mantendo passos de procedimento juntos e **nunca cortando tabelas**. Tamanho-alvo de ~500–800 tokens, com *overlap* de ~10–15% para preservar contexto na fronteira.
- **Metadados ricos por chunk:** fonte, área dona (Operações/Compliance/Comercial), data, **versão** e **rótulo de permissão/ACL** — críticos para o problema de contradição (Seção 12, R1) e para o *security trimming* (Seção 8).
- **Recuperação híbrida (keyword + vetorial):** perguntas de SLA e frete contêm termos exatos (nomes de cliente, códigos, regiões) que a busca puramente semântica erra. O **Azure AI Search** oferece isso nativamente.
- **Recuperar amplo, entregar estreito:** buscar ~30–40 candidatos → reordenar com *reranker* (semantic ranker do Azure AI Search ou Cohere Rerank) → entregar ao LLM apenas os **top 5–10**.

### 5.3. Precisão *vs.* recall (nova na v2)

O reranking resolve **precisão** (ordenar bem o que foi recuperado), mas **não resolve recall**: se o chunk certo não estiver entre os ~30–40 candidatos da primeira etapa, nenhum reranker o traz de volta. O risco de recall concentra-se em perguntas **parafraseadas ou implícitas**, em que o termo exato não aparece. Mitigações: expansão de query/sinônimos (dicionário de termos de negócio — "avaria", "sinistro", nomes comerciais vs. razão social), busca híbrida bem calibrada, e — principalmente — **medir recall@k no conjunto dourado** (Seção 7) antes de assumir que a recuperação funciona.

### 5.4. *Lost in the middle*

A informação posicionada no **meio** de um contexto longo é efetivamente ignorada pelo modelo. Implicações práticas:

1. **Não encher o contexto** — 10 chunks ótimos superam 100 medianos.
2. **Posicionar deliberadamente** — colocar os chunks de maior score no *início* e no *fim* do bloco de contexto, deixando os de menor confiança no meio.
3. **Gerenciar o histórico** — truncar/resumir turnos antigos da conversa para que não empurrem os chunks recuperados para a zona morta central nem consumam orçamento de atenção à toa.

---

## 6. Comportamento do assistente: abstenção, citação e incerteza (nova na v2)

Tão importante quanto recuperar bem é definir **o que o assistente faz quando não tem fonte boa**. Sem essa decisão de design, o sistema troca o erro confiante por extração ruim (Seção 2) pelo erro confiante por **ausência de fonte** — igualmente perigoso.

- **Abstenção explícita.** Quando nenhum chunk recuperado ultrapassa um limiar de relevância, o assistente **não responde por inferência**: declara que não encontrou base e **escala para humano / aponta o canal de dúvida atual** ("perguntar para quem sabe", hoje o fallback da equipe). Melhor "não sei" do que um frete inventado.
- **Citação obrigatória de fonte + data + versão.** Toda resposta factual cita de onde veio e quando a fonte foi atualizada. Isso (a) permite ao atendente verificar, (b) sustenta o tratamento de contradições (R1) e (c) é pré-condição para confiança — que, por sua vez, é o que viabiliza o ganho de tempo (Seção 1).
- **Sinalização de conflito.** Se a recuperação trouxer versões divergentes, o assistente expõe o conflito e prioriza a mais recente por metadado de data, em vez de escolher silenciosamente.
- **Calibração contra viés de automação.** O design de resposta deve **convidar à verificação nos casos de alto risco** (frete/SLA), não desencorajá-la, justamente para que a adoção não vire confiança cega (ver R11, Seção 12).

---

## 7. Avaliação e critérios de aceite (nova na v2 — lacuna crítica da v1)

Para um sistema cuja falha é **silenciosa e confiante**, não existe "viável" sem uma forma objetiva de medir acerto e um limiar de aprovação. Esta seção é pré-requisito de go-live, não um adendo.

**Conjunto dourado (golden set).** Construir, no discovery, **50–100 pares pergunta/resposta reais com gabarito validado por especialista**, por domínio (frete, SLA, devolução). Devem incluir casos difíceis: perguntas sobre tabelas, valores que existem em versões conflitantes, e perguntas sem resposta na base (para testar abstenção).

**Métricas.**
- *Retrieval:* **recall@k** (o chunk certo está entre os k recuperados?) e **precisão do reranker** (o top-5 contém a fonte certa?).
- *Resposta:* **acurácia factual** (a resposta bate com o gabarito?), **taxa de citação correta**, **taxa de abstenção apropriada** (abstém quando deve; não abstém quando não deve) e **taxa de alucinação** (afirma algo sem fonte).

**Critério de aceite (proposta a acordar com a NovaTech).** Por se tratar de frete/SLA, sugere-se exigir, no domínio crítico, **acurácia factual ≥ um patamar acordado (p.ex. ≥ 95%) com taxa de alucinação próxima de zero**, sendo a abstenção preferível ao erro. O número exato é decisão de negócio, mas **tem de existir e ser acordado antes do desenvolvimento** — é ele que liga o sistema à meta de tempo (Seção 1).

**Harness contínuo.** O conjunto dourado roda automaticamente **a cada reindexação mensal** (planilhas/frete mudam todo mês — Seção 2.4) para detectar **regressão**. Sem isso, não há como saber quando o sistema quebrou após uma atualização de fonte.

---

## 8. Segurança, permissões e conformidade (LGPD) (nova na v2)

**Security trimming (permissões em nível de documento).** Numa empresa de ~1.200 pessoas com conteúdo de Compliance e **SLA/preço por cliente**, é provável que nem todo atendente possa ver tudo. Um índice de busca **achata as ACLs do SharePoint/Confluence por padrão** — risco concreto de o assistente expor o SLA ou a tabela de preço de um cliente a quem atende outro. Mitigação: propagar as permissões da fonte como **metadado de ACL no chunk** (Seção 5.2) e filtrar a recuperação pelo perfil do atendente que consulta. *Document-level security* em RAG é reconhecidamente difícil — precisa ser desenhado desde o início, não remendado depois.

**LGPD e residência de dados.** Contexto brasileiro, dados de clientes e operação logística trafegando por Azure OpenAI. Itens a tratar no discovery:
- **Região** em que o Azure OpenAI processará (residência/soberania de dados) e se há restrição contratual da NovaTech quanto a isso.
- **Logging de queries:** o que é registrado, por quanto tempo, com qual base legal — especialmente se as perguntas contiverem dados de cliente.
- **Base legal e finalidade** do tratamento; minimização de dados pessoais nos prompts e logs.
- **Encarregado/DPO da NovaTech** deve validar antes do go-live.

Estes são itens de **viabilidade**, não detalhes de implementação: uma restrição de residência de dados ou um veto do jurídico pode alterar o stack.

---

## 9. Arquitetura recomendada (mapa para o stack Microsoft)

| Camada | Componente | Papel |
|---|---|---|
| Ingestão / parsing | Azure AI Document Intelligence | Extração layout-aware de tabelas + OCR de escaneados |
| Ingestão / wiki | Confluence REST API (formato renderizado) | Resolver macros e preservar grafo de links |
| Dados estruturados | Índice tabular / banco + function calling | Frete e planilhas como lookup determinístico |
| Índice de busca | Azure AI Search (híbrido + semantic ranker) | Recuperação + reranking |
| Segurança | *Security trimming* via metadado de ACL no índice | Filtrar recuperação pelo perfil do atendente (Seção 8) |
| Avaliação | Harness sobre o conjunto dourado | Acurácia/recall por reindexação (Seção 7) |
| Geração | Azure OpenAI (GPT-4o) | Resposta fundamentada, com citação e abstenção (Seção 6) |
| Front-end | Teams (ver nota sobre Copilot Studio) | Interface no fluxo de trabalho do atendente |

Observação de design coerente com o foco em gerenciamento de contexto: **nem tudo deve ser RAG**. Conteúdo determinístico (frete, SLA tabular) deve ser servido por tool/function calling; texto procedimental e normativo é o que efetivamente passa pelo pipeline de recuperação.

**Tensão a decidir no discovery — Copilot Studio vs. pipeline custom (nova na v2).** O front-end no Teams pode sair por dois caminhos com implicações distintas:
- **Copilot Studio:** rápido de subir, mas **low-code e opinativo** — pode não acomodar bem o pipeline custom de recuperação híbrida + reranking + function calling + security trimming + abstenção que este documento descreve.
- **Bot custom (Bot Framework / app Teams)** chamando o pipeline próprio: mais controle e aderência ao desenho acima, ao custo de mais engenharia.

Não dá para ter os dois benefícios de graça. A escolha deve ser **explícita no discovery**, porque define o esforço de desenvolvimento (e, portanto, o cronograma da Seção 11). A recomendação preliminar, dada a exigência de controle sobre recuperação e segurança, pende para o **bot custom**.

---

## 10. Custo (ordem de grandeza) (nova na v2)

Uma análise de viabilidade precisa de pelo menos a **ordem de grandeza** do custo. Os valores abaixo são um **modelo**, não cotação — as tarifas exatas devem ser confirmadas no pricing vigente do Azure (variam por região e tier).

**Drivers de custo.**
- **Ingestão (majoritariamente custo único + reprocessamento eventual):** Document Intelligence (modelo Layout) por página × ~8.000 páginas; embeddings do corpus efetivo. Dominado pelo OCR/Layout; é um gasto pontual, repetido apenas quando documentos mudam.
- **Recorrente mensal (driver principal):** inferência do Azure OpenAI **por query**. Estimativa de tráfego: ~190 queries/dia × ~8K tokens de entrada (chunks + prompt + histórico) + ~0,5K de saída ≈ **~1,6M tokens/dia ≈ ~35M tokens/mês de entrada**. Some reindexação mensal (planilhas/frete) e o **tier fixo do Azure AI Search** (custo mensal fixo, escolhido pelo volume/recursos como o semantic ranker).
- **Reranker** (se Cohere via API, em vez do semantic ranker nativo): custo por chamada.

**Conclusão de magnitude.** Espera-se um **recorrente na casa de baixos milhares de reais/mês**, dominado pela inferência por query e pelo tier do Azure AI Search; a ingestão é predominantemente **custo único**. Isso precisa ser **confirmado contra o pricing atual e o tráfego real medido no piloto** — mas a ordem de grandeza não tende a ser um impeditivo de viabilidade. O ponto da v2 é que **o número precisa constar**, ainda que como faixa.

---

## 11. Cronograma, dependências e propriedade operacional (nova/expandida na v2)

**Por que 3 meses é apertado de verdade.** A v1 tratava o prazo como "factível para um MVP". O ajuste:

1. **O MVP é o núcleo difícil, não uma fatia leve.** Frete + SLA + devolução concentram tabelas de 15+ colunas, OCR e o ETL de dados estruturados — exatamente os itens de maior risco técnico. Escolhemos essa fatia por **valor e risco** (correto), mas isso significa que o MVP enfrenta o pior logo de início, sem um "aquecimento" simples.
2. **Discovery + governança consomem semanas de relógio.** Alinhar Operações, Compliance e Comercial num processo unificado de versão (pré-requisito de R1) é mudança organizacional — raramente rápida. Estimar **4–6 semanas** só para discovery + acordo de governança é prudente.
3. **Dependências do lado da NovaTech (não controladas pela DB1):** migração de documentos críticos para texto nativo (Seção 2.2), fornecimento e validação de dados de frete, validação do conjunto dourado por especialista (Seção 7), aprovação do jurídico/DPO (Seção 8). Cada uma é um gargalo de cronograma.

**Sequenciamento sugerido (dentro dos 3 meses):**
- **Semanas 1–5:** discovery dirigido + acordo de governança + montagem do conjunto dourado + decisão Copilot Studio vs. custom (Seção 9).
- **Semanas 4–10:** construção do pipeline (ingestão/Document Intelligence, ETL estruturado de frete, Confluence, busca híbrida + reranking, abstenção, security trimming) — com o harness de avaliação rodando desde cedo.
- **Semanas 9–12:** hardening, atingir o critério de aceite no conjunto dourado, piloto restrito e go-live faseado.

Se as dependências do cliente atrasarem, **o escopo do MVP encolhe antes de o prazo estourar** (p.ex., entregar SLA + devolução e adiar frete, que é o de maior ETL). Isso deve ser combinado com a NovaTech de antemão.

**Propriedade operacional pós go-live.** Definir **quem é dono** da operação depois que a DB1 sair: reindexação mensal, monitoramento de regressão (harness), atualização do conjunto dourado, tratamento de conflitos sinalizados, ajuste de ACLs. Sem dono claro, o sistema degrada silenciosamente conforme as fontes mudam.

---

## 12. Riscos e premissas

**R1 — Contradição entre documentos (risco principal, de governança).** RAG não resolve a contradição entre versões — ele a propaga fielmente. Hoje a equipe resolve "perguntando para quem sabe"; se as fontes se contradizem, o assistente recuperará as duas versões e ou escolherá arbitrariamente ou apresentará respostas inconsistentes — o mesmo problema, agora automatizado e com aparência de autoridade.
*Mitigação:* priorizar a versão mais recente via metadado de data; sempre citar fonte + data; sinalizar conflitos detectados ao atendente.
*Causa raiz:* ausência de processo unificado de revisão entre Operações, Compliance e Comercial. **É uma lacuna de governança, não de engenharia.** Deve ser registrada no discovery como pré-requisito ou risco assumido — caso contrário, a diretoria cobrará da DB1 uma consistência que a fonte não possui.

**R2 — Qualidade da extração de tabelas.** Falha aqui produz erros silenciosos em frete/SLA. Mitigação: Document Intelligence + tabelas como chunks atômicos + roteamento de cálculo para lógica determinística.

**R3 — Erros silenciosos de OCR.** Mitigação: thresholds de confiança, revisão humana de baixa confiança, migração de documentos críticos para texto nativo.

**R4 — Obsolescência das planilhas.** Mitigação: reindexação acoplada ao ciclo mensal de atualização + harness de regressão (R6).

**R5 — Prazo de 3 meses.** Reavaliado como **apertado de verdade** (Seção 11): o MVP é o núcleo difícil e há dependências do cliente. Mitigação: sequenciamento com escopo elástico (encolher o MVP antes de estourar o prazo) e acordo prévio sobre qual domínio cai primeiro se houver atraso.

**R6 — Ausência de medição de qualidade (novo).** Sem conjunto dourado, métricas e critério de aceite, "funciona" é opinião, não fato — e regressões após reindexação passam despercebidas. Mitigação: Seção 7, com harness rodando a cada reindexação.

**R7 — Vazamento por permissões achatadas (novo).** Índice sem security trimming pode expor SLA/preço entre clientes. Mitigação: ACL como metadado de chunk e filtro por perfil (Seção 8). Risco de Compliance, não só técnico.

**R8 — LGPD / residência de dados (novo).** Tratamento de dados de cliente em Azure OpenAI sem base legal, região definida e política de logs validadas. Mitigação: revisão do DPO no discovery (Seção 8); pode condicionar o stack.

**R9 — Custo recorrente subestimado/imprevisto (novo).** Sem modelo de custo, surpresas de fatura por query/tier. Mitigação: Seção 10 + medir tráfego real no piloto.

**R10 — Dependências do cliente no caminho crítico (novo).** Migração para texto nativo, validação de gabarito, aprovação jurídica — todas fora do controle da DB1. Mitigação: explicitar como pré-requisitos com prazos acordados; escopo elástico (Seção 11).

**R11 — Viés de automação / excesso de confiança (novo).** Atendentes podem passar a confiar cegamente, transformando erro silencioso em erro propagado. Mitigação: citação obrigatória, design que convida à verificação em alto risco (Seção 6), monitoramento de discordâncias.

**R12 — Propriedade operacional indefinida pós go-live (novo).** Sem dono da reindexação/monitoramento, o sistema degrada conforme as fontes mudam. Mitigação: definir operação e handover na proposta (Seção 11).

**Premissa a validar (P1):** densidade dos PDFs (palavras/página) e **tokens reais em português**. O total da base depende disso e foi estimado, não medido. Validar amostrando 10–15 documentos reais no discovery, **medindo tokens diretamente com o tokenizer** (Seção 3).

---

## 13. Próximos passos sugeridos

1. **Discovery dirigido:** amostrar PDFs reais (validar P1 medindo tokens), mapear o grau de contradição entre versões (dimensionar R1) e inventariar quais planilhas/tabelas devem virar dados estruturados.
2. **Definir e acordar a metodologia de avaliação:** construir o conjunto dourado (50–100 Q&As por domínio) e **acordar o critério de aceite de acurácia** com a NovaTech antes do desenvolvimento (Seção 7).
3. **Acordar o tratamento da lacuna de governança (R1)** e listar as **dependências do cliente** (R10) como pré-requisitos com prazos (texto nativo, validação de gabarito, aprovação do DPO).
4. **Revisão de segurança e LGPD:** desenhar o security trimming e validar residência de dados/logs com o DPO (Seção 8).
5. **Modelo de custo** confirmado contra o pricing vigente (Seção 10).
6. **Decidir Copilot Studio vs. bot custom** (Seção 9), pois define o esforço de desenvolvimento.
7. **Definir o recorte do MVP** (frete + SLA + devolução), o escopo elástico em caso de atraso e o pipeline de atualização mensal + harness de regressão.
8. **Prova de conceito de extração** nas tabelas de frete mais complexas, por ser o ponto de maior risco técnico, já medindo acurácia contra o conjunto dourado.
9. **Definir a propriedade operacional pós go-live** (R12).
