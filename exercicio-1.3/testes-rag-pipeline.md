## Pergunta 1
Qual o prazo de devolução para carga perigosa?

### Chunks:

```markdown
[CHUNK 1]
fonte: POL-001-politica-devolucao.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.2764
chunk_index: 4
conteudo: ### 3.5. Custos de devolução

- Defeito ou erro da NovaTech (carga errada, avaria em trânsito): devolução sem custo para o cliente.
- Desistência do cliente (carga correta, sem defeito): o custo do frete reverso é do cliente, calculado com os mesmos multiplicadores do frete original.
- Prazo expirado (solicitação após 7 dias úteis): não elegível para devolução padrão. Encaminhar ao Comercial para negociação caso a caso.

[CHUNK 2]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.2091
chunk_index: 4
conteudo: ### Item 38 — "Cliente quer saber a política para carga que chegou danificada."
Carga danificada em trânsito tem processo diferente de devolução. O cliente precisa registrar a ocorrência em até 48h após o recebimento, com fotos e laudo se possível. A NovaTech investiga e, se comprovada responsabilidade nossa, reembolsa integralmente. Mas isso passa pelo Jurídico, não pelo atendimento normal — encaminhe para o e-mail sinistros@novatech.com.br.

### Item 41 — "Qual a diferença entre SLA de resposta e SLA de resolução?"
Resposta é quando a gente dá o primeiro retorno ao cliente (mesmo que seja 'estamos verificando'). Resolução é quando o problema é efetivamente resolvido. O Gold tem 2h de resposta e 24h de resolução. Silver é 4h e 48h. Standard é 8h e 72h. Para incidentes críticos, os prazos são menores — veja a tabela SLA-2024.

### Item 45 — "O cliente quer desconto no frete. Posso dar?"
Atendente não tem autonomia para dar desconto. Para clientes com mais de 10 fretes especiais por mês, existe desconto automático na tabela (veja PROC-042). Para outros casos, encaminhe ao Comercial com justificativa.

[CHUNK 3]
fonte: PROC-042-v2-frete-especial-revisado.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.2065
chunk_index: 2
conteudo: ## 3. Prazo de entrega para frete especial

O prazo de entrega para frete especial é calculado como o prazo padrão da rota + 3 dias úteis adicionais para manuseio e roteirização de carga pesada (anteriormente era + 2 dias na versão anterior).

## 4. Condições especiais

- Cargas acima de 5.000kg requerem aprovação prévia do gerente de operações regional.
- Cargas perigosas com peso acima de 500kg seguem tabela específica (PROC-043: Frete de Cargas Perigosas). Nota: a PROC-043 está em processo de revisão pelo Compliance e pode sofrer alterações.
- Descontos de volume: a partir de 8 fretes especiais/mês para o mesmo cliente, aplicar desconto de 5% sobre o multiplicador regional. Acima de 15 fretes/mês, desconto de 10%. Descontos maiores requerem aprovação da Diretoria Comercial.

## 5. Disposições transitórias

Durante o período de transição, chamados abertos antes de 01/12/2023 que ainda estejam em processamento devem usar os multiplicadores da versão anterior (PROC-042 v1). Chamados novos a partir de 01/12/2023 devem usar os multiplicadores desta versão.

[CHUNK 4]
fonte: POL-001-politica-devolucao.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.1829
chunk_index: 2
conteudo: ## 3. Regras de Devolução

### 3.1. Prazo geral

O cliente pode solicitar a devolução de mercadorias em até 7 (sete) dias úteis após a data de recebimento confirmada no sistema de tracking. A contagem de dias úteis exclui sábados, domingos e feriados nacionais.

### 3.2. Exceções ao prazo geral

As seguintes categorias de carga NÃO são elegíveis para devolução pelo processo padrão:

- Cargas perigosas classificadas nas classes 1 a 6 da ANTT (Agência Nacional de Transportes Terrestres), conforme Resolução ANTT nº 5.947/2021. Inclui: explosivos (classe 1), gases (classe 2), líquidos inflamáveis (classe 3), sólidos inflamáveis (classe 4), oxidantes e peróxidos (classe 5), substâncias tóxicas e infectantes (classe 6).
- Cargas refrigeradas que tenham rompido a cadeia de frio (temperatura fora da faixa especificada na nota fiscal por mais de 30 minutos contínuos, conforme registro do sensor IoT).
- Cargas com lacre de segurança violado, salvo quando a violação for documentada no ato de entrega com assinatura do motorista e do recebedor.

Para essas categorias, o cliente deve entrar em contato com o setor de Gestão de Riscos (ramal 4500) para tratamento individual.

[CHUNK 5]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.1542
chunk_index: 3
conteudo: ### Item 22 — "Cliente quer saber sobre seguro de carga. O que falar?"
A NovaTech oferece seguro de carga como adicional. O valor é 0,3% do valor declarado da mercadoria para cargas padrão e 0,8% para cargas perigosas. Detalhe: isso vale para contratos a partir de 2023. Contratos mais antigos podem ter percentuais diferentes — confirme com o Comercial.

### Item 27 — "O tracking mostra 'em trânsito' há 5 dias. O que faço?"
Depende da rota. Rotas para o Norte podem levar até 10 dias úteis. Para Sul/Sudeste, mais de 3 dias parado é estranho. Abra um chamado de rastreamento e classifique como prioridade alta se for Gold ou se o valor da carga for acima de R$ 50.000.

### Item 32 — "Pode enviar carga perigosa com frete expresso?"
Sim, mas precisa de autorização do Compliance e a documentação ANTT tem que estar atualizada. Na prática, demora uns 2 dias para conseguir a autorização, então o 'expresso' acaba não sendo tão expresso. Avise o cliente sobre isso.

```

### Resposta Claude (Haiku 4.5 Extended):

Carga perigosa não segue o prazo padrão de devolução — ela está fora dele. Cargas perigosas classificadas nas **classes 1 a 6 da ANTT** (Resolução ANTT nº 5.947/2021) **não são elegíveis para devolução pelo processo padrão**. Nesses casos, o cliente deve acionar a **Gestão de Riscos (ramal 4500)** para tratamento caso a caso.

(Fonte: POL-001 Política de Devolução, seção 3.2 — área e versão não informadas nos metadados.)

Observação: a documentação trata explicitamente das classes 1 a 6; para carga perigosa de outra classe, não há previsão nos trechos que tenho — aí seria melhor confirmar com a área responsável.

Por ser condição de devolução, confirme antes de garantir ao cliente.

### Análise:

#### 1. Mapeamento dos chunks recuperados → gabarito

| Recuperado | Equivale a (Anexo B) | Veredito |
|---|---|---|
| CHUNK 4 — POL-001 idx 2 (3.1 + 3.2) | **POL-001-A + POL-001-B** | ✅ alvo principal — os dois obrigatórios vieram fundidos num só chunk |
| CHUNK 1 — POL-001 idx 4 (3.5 Custos) | POL-001-D | ⚠️ tangencial (devolução, mas custo ≠ prazo) |
| CHUNK 5 — FAQ idx 3 (item 32) | FAQ-32 | ❌ ruído — "carga perigosa" sim, mas *frete expresso*, não devolução |
| CHUNK 2 — FAQ idx 4 (item 38) | FAQ-38 | ❌ ruído — carga *danificada*, processo distinto |
| CHUNK 3 — PROC-042-v2 idx 2 | PROC-042v2-C/D/E | ❌ ruído — frete especial |

**Recall dos obrigatórios: 100%** (a resposta era plenamente respondível). Mas a qualidade do retrieval é medíocre por três motivos:

- **FAQ-03 não foi recuperado.** Esse era *o* item de FAQ feito sob medida para "devolução de carga perigosa". No lugar dele entrou o FAQ-32 (frete expresso). É um near-miss semântico clássico: o embedding pegou "carga perigosa" mas errou a intenção (devolução vs. expedição).
- **Inversão de ranking.** O maior score (0.2764) é o chunk de *custos* (CHUNK 1), enquanto o chunk decisivo (CHUNK 4, com 3.1+3.2) aparece só em 4º lugar com 0.1829. O retriever está ordenando mal para essa query.
- **Scores baixos e comprimidos** (0.15–0.28, todos juntinhos). Pouca separação entre sinal e ruído — sintoma de embedding/query mal calibrados. Precisão efetiva: 1 de 5 chunks realmente no alvo.

Nota de chunking: no seu pipeline real, POL-001-A e POL-001-B estão **no mesmo chunk** (idx 2), enquanto o Anexo B os trata separados. Isso ajudou aqui (recuperou os dois de uma vez), mas vale registrar que o gabarito assume granularidade mais fina.

#### 2. Avaliação da resposta da LLM

Aqui o resultado é o oposto: **a geração está muito boa**, apesar do retrieval ruidoso.

- **Grounding correto.** A resposta saiu inteira do CHUNK 4 (classes 1–6, Resolução 5.947/2021, ramal 4500). Nada inventado.
- **Não caiu em duas armadilhas do anexo.** Não inverteu a regra (armadilha #4 — disse corretamente que *não* é elegível) e **não usou o FAQ-32** mesmo tendo-o no contexto (armadilha #2 — ignorou o ruído de FAQ para informação crítica). Esse descarte ativo de chunk irrelevante é o melhor sinal da resposta.
- **Reframe da premissa falsa.** A pergunta pressupõe que existe "um prazo para carga perigosa". A LLM corrigiu isso: não há prazo padrão porque a categoria está *fora* do processo. Resposta certa para uma pergunta mal-posta.
- **Hedging adequado:** admitiu metadados ausentes (área/versão), delimitou "classes 1–6" e pediu confirmação. Sem excesso.

Único reparo, menor: ela não ancorou o prazo geral de 7 dias úteis (que está no mesmo CHUNK 4) como contraste — "o padrão é 7 dias, mas perigosa está excluída disso". Por outro lado, dá pra defender a omissão: citar "7 dias" poderia induzir o cliente a achar que há janela de devolução. Aceitável como está.

**Veredito geral:** retrieval aprovado no mínimo necessário mas com qualidade fraca (corrija ranking/embedding e investigue por que FAQ-03 perde para FAQ-32); geração exemplar. Se quiser, posso montar um caso de teste para isolar o problema de retrieval — por exemplo, rodar a mesma query com FAQ-03 forçado no contexto para confirmar que o gargalo é o retriever e não o gerador.

## Pergunta 2
Meu cliente é Gold, qual o SLA de resolução?

### Chunks:

```markdown
[CHUNK 1]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.3389
chunk_index: 4
conteudo: ### Item 38 — "Cliente quer saber a política para carga que chegou danificada."
Carga danificada em trânsito tem processo diferente de devolução. O cliente precisa registrar a ocorrência em até 48h após o recebimento, com fotos e laudo se possível. A NovaTech investiga e, se comprovada responsabilidade nossa, reembolsa integralmente. Mas isso passa pelo Jurídico, não pelo atendimento normal — encaminhe para o e-mail sinistros@novatech.com.br.

### Item 41 — "Qual a diferença entre SLA de resposta e SLA de resolução?"
Resposta é quando a gente dá o primeiro retorno ao cliente (mesmo que seja 'estamos verificando'). Resolução é quando o problema é efetivamente resolvido. O Gold tem 2h de resposta e 24h de resolução. Silver é 4h e 48h. Standard é 8h e 72h. Para incidentes críticos, os prazos são menores — veja a tabela SLA-2024.

### Item 45 — "O cliente quer desconto no frete. Posso dar?"
Atendente não tem autonomia para dar desconto. Para clientes com mais de 10 fretes especiais por mês, existe desconto automático na tabela (veja PROC-042). Para outros casos, encaminhe ao Comercial com justificativa.

[CHUNK 2]
fonte: SLA-2024-tabela-sla-clientes.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.2618
chunk_index: 1
conteudo: # SLA-2024 — Tabela de SLA por Tipo de Cliente

**Versão:** 2024.1
**Última atualização:** 02/01/2024
**Responsável:** Diretoria Comercial + Diretoria de Operações
**Classificação:** Documento contratual — os SLAs listados aqui são compromissos formais com o cliente

## 1. Classificação de clientes

A NovaTech classifica seus clientes em 3 (três) tiers com base no volume mensal de operações e no valor do contrato:

| Tier | Critério de elegibilidade | Revisão |
|------|--------------------------|---------|
| Gold | Contrato anual acima de R$ 500.000 OU mais de 200 operações/mês | Semestral |
| Silver | Contrato anual entre R$ 100.000 e R$ 500.000 OU entre 50 e 200 operações/mês | Semestral |
| Standard | Todos os demais clientes | Anual |

Nota: Não existem outros tiers além dos três listados acima. Solicitações de SLA diferenciado fora desses tiers devem ser encaminhadas ao Comercial para análise de viabilidade.

[CHUNK 3]
fonte: SLA-2024-tabela-sla-clientes.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.1000
chunk_index: 3
conteudo: ## 4. Penalidades por descumprimento

- Primeira violação de SLA no mês: registro interno, sem impacto contratual.
- Segunda violação no mesmo mês: crédito de 5% sobre o valor do frete do chamado afetado.
- Terceira violação ou mais no mesmo mês: crédito de 10% + reunião obrigatória com o gerente de conta (Gold) ou gerente de operações (Silver/Standard).

## 5. Medição e reportes

Os SLAs são medidos pelo sistema de chamados (Azure DevOps) a partir do timestamp de abertura do chamado. O relógio de SLA pausa fora do horário comercial (08h-18h, dias úteis) para chamados gerais, mas não pausa para incidentes críticos de clientes Gold.

[CHUNK 4]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0166
chunk_index: 2
conteudo: ## Perguntas selecionadas (das 47 do documento original)

### Item 3 — "Cliente perguntou se pode devolver carga perigosa. O que respondo?"
Na prática, a gente orienta o cliente a ligar no ramal 4500 (Gestão de Riscos). Oficialmente não pode pelo processo padrão, mas já tiveram casos em que o pessoal de Riscos autorizou exceção. Então não diga que é impossível — diga que precisa de tratamento especial.

### Item 8 — "Como funciona o frete especial?"
Acima de 500kg, aplica a tabela de multiplicadores por região. Cuidado: existem duas versões da PROC-042. A mais recente tem multiplicadores mais altos. Na dúvida, use a mais recente (v2), mas se o cliente reclamar do valor, pode ser que o contrato dele ainda esteja na tabela antiga.

### Item 15 — "Cliente diz que é Platinum. Existe esse tier?"
Não existe tier Platinum na NovaTech. Às vezes o cliente confunde com outra transportadora ou com o programa de fidelidade antigo que foi descontinuado em 2022. Oriente que nossos tiers são Gold, Silver e Standard e peça o número do contrato para verificar.

[CHUNK 5]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0150
chunk_index: 3
conteudo: ### Item 22 — "Cliente quer saber sobre seguro de carga. O que falar?"
A NovaTech oferece seguro de carga como adicional. O valor é 0,3% do valor declarado da mercadoria para cargas padrão e 0,8% para cargas perigosas. Detalhe: isso vale para contratos a partir de 2023. Contratos mais antigos podem ter percentuais diferentes — confirme com o Comercial.

### Item 27 — "O tracking mostra 'em trânsito' há 5 dias. O que faço?"
Depende da rota. Rotas para o Norte podem levar até 10 dias úteis. Para Sul/Sudeste, mais de 3 dias parado é estranho. Abra um chamado de rastreamento e classifique como prioridade alta se for Gold ou se o valor da carga for acima de R$ 50.000.

### Item 32 — "Pode enviar carga perigosa com frete expresso?"
Sim, mas precisa de autorização do Compliance e a documentação ANTT tem que estar atualizada. Na prática, demora uns 2 dias para conseguir a autorização, então o 'expresso' acaba não sendo tão expresso. Avise o cliente sobre isso.

```

### Resposta Claude (Haiku 4.5 Extended):

Para Gold, a resolução é **até 24h** em chamado geral (e **até 4h** em incidente crítico).
(Fonte: SLA-2024, Diretoria Comercial + Diretoria de Operações, v2024.1.)

Posso detalhar o que conta como incidente crítico, se precisar.

Por ser SLA, valide no contrato antes de comunicar ao cliente.

### Análise:

Esse caso é bem mais grave que o anterior — e perigoso justamente porque a resposta *parece* impecável. **Reprova em groundedness, apesar dos números estarem certos.** Vou mostrar por quê.

#### 1. Retrieval: falhou no chunk obrigatório

Pelo gabarito, *"SLA do cliente Gold"* exige **SLA-2024-B** (a tabela de SLAs de chamados gerais — onde está, de forma contratual, "Gold: resolução 24h"). Esse chunk **não foi recuperado**. Nem o SLA-2024-C (incidentes críticos).

| Recuperado | Equivale a (Anexo B) | Veredito |
|---|---|---|
| CHUNK 1 — FAQ idx 4 (itens 38/41/45) — score 0.3389 | FAQ-38 + itens 41/45 | ⚠️ o item 41 traz o "Gold: 24h de resolução", mas é **FAQ informal**, não a tabela contratual |
| CHUNK 2 — SLA-2024 idx 1 (cabeçalho + Seção 1) — 0.2618 | SLA-2024-A | ✅ recuperado, mas é só **classificação de tiers** — não tem tempos de SLA |
| CHUNK 3 — SLA-2024 idx 3 (Seções 4 e 5) — 0.1000 | SLA-2024-E + medição | ❌ penalidades/medição — sem os tempos de resolução |
| CHUNK 4 — FAQ idx 2 (itens 3/8/15) — 0.0166 | FAQ-03/08/15 | ❌ ruído |
| CHUNK 5 — FAQ idx 3 (itens 22/27/32) — 0.0150 | FAQ-22/27/32 | ❌ ruído |

**Recall dos obrigatórios: 0%.** O único chunk que responde a pergunta de forma autoritativa (SLA-2024-B) nem apareceu no top-5. Note ainda a inversão de ranking: o topo (0.3389) é um *bundle* de FAQ, e a tabela de SLA contratual está ausente.

#### 2. Onde a LLM realmente foi buscar cada número

Aqui está o problema de fundo. Rastreando a resposta contra o que estava no contexto:

- **"resolução até 24h (chamado geral)"** → existe sim no contexto, mas **só no CHUNK 1, item 41 do FAQ** ("O Gold tem 2h de resposta e 24h de resolução"). A fonte contratual (SLA-2024-B) não foi recuperada. Procedência fraca — e exatamente a armadilha #2 do anexo: usar FAQ informal para informação que é **compromisso contratual formal**.
- **"até 4h em incidente crítico"** → **não está em nenhum dos 5 chunks recuperados.** O item 41 só diz "para incidentes críticos os prazos são menores — veja a tabela SLA-2024", sem dar o número. O CHUNK 3 cita "incidentes críticos de clientes Gold" apenas no contexto de pausa de relógio, sem tempo de resolução. Ou seja: **o "4h" foi alucinado** (conhecimento paramétrico/vazamento), e por acaso bate com o gabarito.

#### 3. A citação é fabricada

A resposta credita: *"(Fonte: SLA-2024, Diretoria Comercial + Diretoria de Operações, v2024.1.)"*. Esses metadados vêm do **CHUNK 2** — que contém **apenas a classificação de tiers, nenhum tempo de SLA**. A LLM pegou os números de outro lugar (FAQ + alucinação) e atribuiu a um chunk autoritativo que não os contém. Isso dá uma **falsa aparência de procedência contratual** a um número inventado. É o tipo de citação que engana o avaliador e o atendente.

#### Veredito

Esse é o caso clássico de **"resposta certa pelo motivo errado"**: os números coincidem com a documentação, então uma avaliação ingênua de *correctness* marcaria PASS. Uma avaliação rigorosa de *groundedness* marca **FAIL** — o "4h" não tem lastro no contexto, o "24h" veio de fonte informal em vez da contratual, e a citação aponta para um chunk que não sustenta nenhum dos dois. Em produção, com outra pergunta onde o conhecimento paramétrico não acertar por sorte, esse mesmo comportamento produz um número errado com cara de oficial.

Diferença prática entre os dois testes: no caso da carga perigosa, retrieval medíocre + geração disciplinada (descartou ruído, sem inventar). Aqui, retrieval falho + geração indisciplinada (preencheu a lacuna com memória e mascarou com citação). O gerador deveria ter dito que só tinha o número geral (e de fonte secundária) e que a tabela crítica não estava no contexto.

Sugestão de correção em duas frentes: (1) descobrir por que SLA-2024-B/-C não entram no top-k — provavelmente chunking ou embedding da tabela; e (2) endurecer o prompt de geração para citar apenas o chunk de onde o número saiu e abster-se quando o valor não estiver no contexto. Quer que eu escreva um caso de teste de groundedness que pegue justamente esse padrão (número plausível sem chunk de suporte)?

## Pergunta 3

### Chunks:

```markdown
[CHUNK 1]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0879
chunk_index: 3
conteudo: ### Item 22 — "Cliente quer saber sobre seguro de carga. O que falar?"
A NovaTech oferece seguro de carga como adicional. O valor é 0,3% do valor declarado da mercadoria para cargas padrão e 0,8% para cargas perigosas. Detalhe: isso vale para contratos a partir de 2023. Contratos mais antigos podem ter percentuais diferentes — confirme com o Comercial.

### Item 27 — "O tracking mostra 'em trânsito' há 5 dias. O que faço?"
Depende da rota. Rotas para o Norte podem levar até 10 dias úteis. Para Sul/Sudeste, mais de 3 dias parado é estranho. Abra um chamado de rastreamento e classifique como prioridade alta se for Gold ou se o valor da carga for acima de R$ 50.000.

### Item 32 — "Pode enviar carga perigosa com frete expresso?"
Sim, mas precisa de autorização do Compliance e a documentação ANTT tem que estar atualizada. Na prática, demora uns 2 dias para conseguir a autorização, então o 'expresso' acaba não sendo tão expresso. Avise o cliente sobre isso.

[CHUNK 2]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0457
chunk_index: 4
conteudo: ### Item 38 — "Cliente quer saber a política para carga que chegou danificada."
Carga danificada em trânsito tem processo diferente de devolução. O cliente precisa registrar a ocorrência em até 48h após o recebimento, com fotos e laudo se possível. A NovaTech investiga e, se comprovada responsabilidade nossa, reembolsa integralmente. Mas isso passa pelo Jurídico, não pelo atendimento normal — encaminhe para o e-mail sinistros@novatech.com.br.

### Item 41 — "Qual a diferença entre SLA de resposta e SLA de resolução?"
Resposta é quando a gente dá o primeiro retorno ao cliente (mesmo que seja 'estamos verificando'). Resolução é quando o problema é efetivamente resolvido. O Gold tem 2h de resposta e 24h de resolução. Silver é 4h e 48h. Standard é 8h e 72h. Para incidentes críticos, os prazos são menores — veja a tabela SLA-2024.

### Item 45 — "O cliente quer desconto no frete. Posso dar?"
Atendente não tem autonomia para dar desconto. Para clientes com mais de 10 fretes especiais por mês, existe desconto automático na tabela (veja PROC-042). Para outros casos, encaminhe ao Comercial com justificativa.

[CHUNK 3]
fonte: PROC-042-v2-frete-especial-revisado.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0039
chunk_index: 2
conteudo: ## 3. Prazo de entrega para frete especial

O prazo de entrega para frete especial é calculado como o prazo padrão da rota + 3 dias úteis adicionais para manuseio e roteirização de carga pesada (anteriormente era + 2 dias na versão anterior).

## 4. Condições especiais

- Cargas acima de 5.000kg requerem aprovação prévia do gerente de operações regional.
- Cargas perigosas com peso acima de 500kg seguem tabela específica (PROC-043: Frete de Cargas Perigosas). Nota: a PROC-043 está em processo de revisão pelo Compliance e pode sofrer alterações.
- Descontos de volume: a partir de 8 fretes especiais/mês para o mesmo cliente, aplicar desconto de 5% sobre o multiplicador regional. Acima de 15 fretes/mês, desconto de 10%. Descontos maiores requerem aprovação da Diretoria Comercial.

## 5. Disposições transitórias

Durante o período de transição, chamados abertos antes de 01/12/2023 que ainda estejam em processamento devem usar os multiplicadores da versão anterior (PROC-042 v1). Chamados novos a partir de 01/12/2023 devem usar os multiplicadores desta versão.

[CHUNK 4]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: -0.0185
chunk_index: 2
conteudo: ## Perguntas selecionadas (das 47 do documento original)

### Item 3 — "Cliente perguntou se pode devolver carga perigosa. O que respondo?"
Na prática, a gente orienta o cliente a ligar no ramal 4500 (Gestão de Riscos). Oficialmente não pode pelo processo padrão, mas já tiveram casos em que o pessoal de Riscos autorizou exceção. Então não diga que é impossível — diga que precisa de tratamento especial.

### Item 8 — "Como funciona o frete especial?"
Acima de 500kg, aplica a tabela de multiplicadores por região. Cuidado: existem duas versões da PROC-042. A mais recente tem multiplicadores mais altos. Na dúvida, use a mais recente (v2), mas se o cliente reclamar do valor, pode ser que o contrato dele ainda esteja na tabela antiga.

### Item 15 — "Cliente diz que é Platinum. Existe esse tier?"
Não existe tier Platinum na NovaTech. Às vezes o cliente confunde com outra transportadora ou com o programa de fidelidade antigo que foi descontinuado em 2022. Oriente que nossos tiers são Gold, Silver e Standard e peça o número do contrato para verificar.

[CHUNK 5]
fonte: PROC-042-frete-especial-v1.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: -0.0197
chunk_index: 2
conteudo: ## 4. Condições especiais

- Cargas acima de 5.000kg requerem aprovação prévia do gerente de operações regional.
- Cargas perigosas com peso acima de 500kg seguem tabela específica (PROC-043: Frete de Cargas Perigosas).
- Descontos de volume (mais de 10 fretes especiais/mês para o mesmo cliente) devem ser negociados pelo Comercial e registrados em aditivo contratual.

```

### Resposta Claude (Haiku 4.5 Extended):

Não consigo fechar o valor: a documentação traz que frete acima de 500kg usa multiplicadores por região, e 600kg se encaixa nisso. Mas **não constam nos chunks** o multiplicador específico para Manaus (região Norte) nem o valor base de frete — e eu não invento a parte que falta.

Os parâmetros que constam são:
- **Enquadramento:** frete especial (acima de 500kg) — *(Fonte: PROC-042-v2, seção 3)*
- **Aplicação:** tabela de multiplicadores por região — *(Fonte: FAQ-atendimento, item 8)*

Para o valor final, confirme com `[Operações]` ou `[área responsável]`. 

**Por ser frete, confirme na tabela de preços antes de comunicar ao cliente.**

### Análise:

O retriever falhou de novo (recall 0% nos obrigatórios), mas aqui o gerador **acertou em cheio** — abstenção limpa, sem inventar número. Mesmo modo de falha no retrieval, comportamento oposto na geração.

#### 1. Retrieval

Pelo gabarito, *"frete 600kg para Manaus"* exige **PROC-042v2-A** (a fórmula) + **PROC-042v2-B** (os multiplicadores, com Norte 1.8). **Nenhum dos dois foi recuperado.**

| Recuperado | Equivale a (Anexo B) | Score | Veredito |
|---|---|---|---|
| CHUNK 1 — FAQ idx 3 (22/27/32) | FAQ-22/27/32 | 0.0879 | ❌ ruído (item 27 fala de *prazo* p/ Norte, não custo) |
| CHUNK 2 — FAQ idx 4 (38/41/45) | FAQ-38/41/45 | 0.0457 | ❌ ruído (item 45 toca em desconto, sem números) |
| CHUNK 3 — PROC-042-v2 idx 2 (Seções 3/4/5) | PROC-042v2-C/D/E | 0.0039 | ⚠️ é a v2, mas **prazo/condições/transição** — não a fórmula nem os multiplicadores |
| CHUNK 4 — FAQ idx 2 (3/8/15) | FAQ-03/08/15 | -0.0185 | ⚠️ item 8 confirma o *enquadramento* (>500kg → multiplicadores), mas sem valores |
| CHUNK 5 — PROC-042 **v1** idx 2 (Seção 4) | — | -0.0197 | ❌ ruído + armadilha de versão (v1 no contexto) |

Repare nos **scores quase-zero e negativos** (0.0879 até -0.0197). O retriever literalmente não encontrou nada relevante e isso está visível no sinal — um *threshold* de corte teria sinalizado "sem resultados úteis" corretamente aqui. As Seções 2 e 2.1 da PROC-042-v2 (fórmula + Norte 1.8) não entraram no top-k; provável problema de chunking/embedding da tabela, igual ao caso do SLA.

Detalhe estrutural importante: mesmo com retrieval perfeito, **um valor final em R$ seria impossível** — o *valor base* do frete não está documentado em lugar nenhum do Anexo B. O melhor obtível seria a fórmula "base × 1.8 × 1.0", com a base desconhecida. É a "pergunta sem cobertura parcial" (armadilha #5).

#### 2. Geração

A resposta acerta tudo o que importa:

- **Não inventou número.** "Eu não invento a parte que falta" — exatamente o comportamento esperado na armadilha #5.
- **Separou o que tem do que falta** com precisão: enquadramento (frete especial >500kg) e mecanismo (multiplicadores por região) estão no contexto; o **multiplicador do Norte** e o **valor base** não estão. Ela inclusive nomeou a lacuna do valor base, que é o gargalo estrutural real.
- **Não caiu na contradição v1/v2** (armadilha #1): com a v1 e a v2 ambas no contexto, abster-se de calcular evitou misturar multiplicadores.
- **Sourcing honesto:** usou o FAQ item 8 só para o *enquadramento*, não para um número, e foi transparente quanto a isso. Encaminhamento correto a Operações.

Um reparo menor: a citação *"frete especial (acima de 500kg) — PROC-042-v2, seção 3"* é frouxa — a seção 3 trata de **prazo**; o limiar de 500kg e a fórmula estão na seção 2 (não recuperada) e são reafirmados no FAQ item 8. Não é fabricação como no caso do SLA (cita um doc que está mesmo no contexto), apenas atribuição imprecisa de seção. Vale apertar para "cite a seção exata de onde saiu a afirmação".

## Pergunta 4
Qual o ramal do CEO?

### Chunks:

```markdown
[CHUNK 1]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: -0.3370
chunk_index: 4
conteudo: ### Item 38 — "Cliente quer saber a política para carga que chegou danificada."
Carga danificada em trânsito tem processo diferente de devolução. O cliente precisa registrar a ocorrência em até 48h após o recebimento, com fotos e laudo se possível. A NovaTech investiga e, se comprovada responsabilidade nossa, reembolsa integralmente. Mas isso passa pelo Jurídico, não pelo atendimento normal — encaminhe para o e-mail sinistros@novatech.com.br.

### Item 41 — "Qual a diferença entre SLA de resposta e SLA de resolução?"
Resposta é quando a gente dá o primeiro retorno ao cliente (mesmo que seja 'estamos verificando'). Resolução é quando o problema é efetivamente resolvido. O Gold tem 2h de resposta e 24h de resolução. Silver é 4h e 48h. Standard é 8h e 72h. Para incidentes críticos, os prazos são menores — veja a tabela SLA-2024.

### Item 45 — "O cliente quer desconto no frete. Posso dar?"
Atendente não tem autonomia para dar desconto. Para clientes com mais de 10 fretes especiais por mês, existe desconto automático na tabela (veja PROC-042). Para outros casos, encaminhe ao Comercial com justificativa.

[CHUNK 2]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: -0.3571
chunk_index: 2
conteudo: ## Perguntas selecionadas (das 47 do documento original)

### Item 3 — "Cliente perguntou se pode devolver carga perigosa. O que respondo?"
Na prática, a gente orienta o cliente a ligar no ramal 4500 (Gestão de Riscos). Oficialmente não pode pelo processo padrão, mas já tiveram casos em que o pessoal de Riscos autorizou exceção. Então não diga que é impossível — diga que precisa de tratamento especial.

### Item 8 — "Como funciona o frete especial?"
Acima de 500kg, aplica a tabela de multiplicadores por região. Cuidado: existem duas versões da PROC-042. A mais recente tem multiplicadores mais altos. Na dúvida, use a mais recente (v2), mas se o cliente reclamar do valor, pode ser que o contrato dele ainda esteja na tabela antiga.

### Item 15 — "Cliente diz que é Platinum. Existe esse tier?"
Não existe tier Platinum na NovaTech. Às vezes o cliente confunde com outra transportadora ou com o programa de fidelidade antigo que foi descontinuado em 2022. Oriente que nossos tiers são Gold, Silver e Standard e peça o número do contrato para verificar.

[CHUNK 3]
fonte: POL-001-politica-devolucao.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: -0.3729
chunk_index: 3
conteudo: ### 3.3. Procedimento de devolução

1. O cliente abre chamado no Portal do Cliente (portal.novatech.com.br), selecionando a categoria "Devolução de Mercadoria".
2. O chamado deve incluir: número do CT-e (Conhecimento de Transporte Eletrônico), fotos da mercadoria no estado atual (mínimo 3 fotos: embalagem externa, etiqueta de identificação, e conteúdo), e motivo da devolução.
3. O time de atendimento tem 4 horas úteis para triagem do chamado (verificar elegibilidade, documentação e prazo).
4. Se elegível, a coleta reversa é agendada em até 2 dias úteis após aprovação.
5. O reembolso ou crédito é processado em até 5 dias úteis após o recebimento da mercadoria devolvida no centro de distribuição.

### 3.4. Devoluções parciais

Quando a entrega envolver múltiplos volumes, o cliente pode devolver volumes individuais. Cada volume devolvido segue o mesmo procedimento da seção 3.3. O cálculo de reembolso é proporcional ao peso/valor do volume devolvido, conforme o CT-e.

[CHUNK 4]
fonte: SLA-2024-tabela-sla-clientes.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: -0.4010
chunk_index: 1
conteudo: # SLA-2024 — Tabela de SLA por Tipo de Cliente

**Versão:** 2024.1
**Última atualização:** 02/01/2024
**Responsável:** Diretoria Comercial + Diretoria de Operações
**Classificação:** Documento contratual — os SLAs listados aqui são compromissos formais com o cliente

## 1. Classificação de clientes

A NovaTech classifica seus clientes em 3 (três) tiers com base no volume mensal de operações e no valor do contrato:

| Tier | Critério de elegibilidade | Revisão |
|------|--------------------------|---------|
| Gold | Contrato anual acima de R$ 500.000 OU mais de 200 operações/mês | Semestral |
| Silver | Contrato anual entre R$ 100.000 e R$ 500.000 OU entre 50 e 200 operações/mês | Semestral |
| Standard | Todos os demais clientes | Anual |

Nota: Não existem outros tiers além dos três listados acima. Solicitações de SLA diferenciado fora desses tiers devem ser encaminhadas ao Comercial para análise de viabilidade.

[CHUNK 5]
fonte: PROC-042-frete-especial-v1.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: -0.4040
chunk_index: 2
conteudo: ## 4. Condições especiais

- Cargas acima de 5.000kg requerem aprovação prévia do gerente de operações regional.
- Cargas perigosas com peso acima de 500kg seguem tabela específica (PROC-043: Frete de Cargas Perigosas).
- Descontos de volume (mais de 10 fretes especiais/mês para o mesmo cliente) devem ser negociados pelo Comercial e registrados em aditivo contratual.

```

### Resposta Claude (Haiku 4.5 Extended):

Eu ajudo apenas com a documentação e os procedimentos de atendimento da NovaTech (frete, SLA, devoluções e processos). Para isso aí, melhor usar outro canal.

### Análise:

Esse é o caso mais limpo da série. Pergunta totalmente **fora de domínio** (ramal do CEO não existe em nenhum lugar da base), retrieval sem nada para entregar, e o gerador recusou corretamente sem inventar. Passa.

#### Retrieval:

Não há o que recuperar — nenhum chunk trata de diretório interno/CEO. O retriever devolveu os cinco "menos ruins", e o que importa são os scores:

| Recuperado | Score |
|---|---|
| CHUNK 1 — FAQ idx 4 | -0.3370 |
| CHUNK 2 — FAQ idx 2 | -0.3571 |
| CHUNK 3 — POL-001 idx 3 | -0.3729 |
| CHUNK 4 — SLA-2024 idx 1 | -0.4010 |
| CHUNK 5 — PROC-042 v1 idx 2 | -0.4040 |

**Todos fortemente negativos.** Esse é o padrão de assinatura de pergunta sem cobertura: o melhor match já é -0.337. Comparando a série — perigosa (~0.18–0.28), SLA (~0.0–0.34), Manaus (~0 a -0.02), CEO (-0.34 a -0.40) — fica evidente que o score *já carrega* a informação de "não tenho isso". Isso é o argumento operacional definitivo para um **gate de threshold**: se o score máximo cair abaixo de um corte, o sistema devolve "sem informação relevante" antes mesmo de chamar a LLM, sem depender do julgamento do gerador.

#### Geração:

- **Não inventou ramal.** O ponto crítico. E há uma armadilha de colisão semântica latente: a base tem um ramal real (4500, Gestão de Riscos). Um modelo mais fraco poderia ter agarrado "ramal" e oferecido o 4500 como sendo do CEO. Esse não chegou perto disso. Limpo.
- **Delimitou o escopo** (documentação/atendimento NovaTech) e redirecionou.
- Não fingiu que a resposta estava nos docs.

Vale distinguir esta recusa da abstenção do caso Manaus, porque são dois comportamentos corretos *diferentes*:

- **Manaus** = pergunta *dentro* do escopo, dado específico ausente nos chunks → "eis o que tenho, eis o que falta, escale para Operações."
- **CEO** = pergunta *fora* do escopo → "não é meu domínio, use outro canal."

O gerador escolheu o enquadramento certo para cada um. Um sistema maduro precisa saber separar esses dois — e idealmente o de OOD (CEO) deveria ser pego pelo gate de score, enquanto o de cobertura-parcial (Manaus) precisa do julgamento do gerador porque tem score baixo-mas-não-tão-negativo e contexto parcialmente útil.

Único polimento (não é falha): "melhor usar outro canal" é vago. Para uma ferramenta interna, apontar o diretório corporativo/RH seria mais útil — mas como o assistente honestamente não sabe qual é o canal, a vagueza é defensável.

## Pergunta 5
A carga do cliente foi danificada. Como proceder?

### Chunks:

```markdown
[CHUNK 1]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.2243
chunk_index: 4
conteudo: ### Item 38 — "Cliente quer saber a política para carga que chegou danificada."
Carga danificada em trânsito tem processo diferente de devolução. O cliente precisa registrar a ocorrência em até 48h após o recebimento, com fotos e laudo se possível. A NovaTech investiga e, se comprovada responsabilidade nossa, reembolsa integralmente. Mas isso passa pelo Jurídico, não pelo atendimento normal — encaminhe para o e-mail sinistros@novatech.com.br.

### Item 41 — "Qual a diferença entre SLA de resposta e SLA de resolução?"
Resposta é quando a gente dá o primeiro retorno ao cliente (mesmo que seja 'estamos verificando'). Resolução é quando o problema é efetivamente resolvido. O Gold tem 2h de resposta e 24h de resolução. Silver é 4h e 48h. Standard é 8h e 72h. Para incidentes críticos, os prazos são menores — veja a tabela SLA-2024.

### Item 45 — "O cliente quer desconto no frete. Posso dar?"
Atendente não tem autonomia para dar desconto. Para clientes com mais de 10 fretes especiais por mês, existe desconto automático na tabela (veja PROC-042). Para outros casos, encaminhe ao Comercial com justificativa.

[CHUNK 2]
fonte: POL-001-politica-devolucao.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0494
chunk_index: 4
conteudo: ### 3.5. Custos de devolução

- Defeito ou erro da NovaTech (carga errada, avaria em trânsito): devolução sem custo para o cliente.
- Desistência do cliente (carga correta, sem defeito): o custo do frete reverso é do cliente, calculado com os mesmos multiplicadores do frete original.
- Prazo expirado (solicitação após 7 dias úteis): não elegível para devolução padrão. Encaminhar ao Comercial para negociação caso a caso.

[CHUNK 3]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0455
chunk_index: 2
conteudo: ## Perguntas selecionadas (das 47 do documento original)

### Item 3 — "Cliente perguntou se pode devolver carga perigosa. O que respondo?"
Na prática, a gente orienta o cliente a ligar no ramal 4500 (Gestão de Riscos). Oficialmente não pode pelo processo padrão, mas já tiveram casos em que o pessoal de Riscos autorizou exceção. Então não diga que é impossível — diga que precisa de tratamento especial.

### Item 8 — "Como funciona o frete especial?"
Acima de 500kg, aplica a tabela de multiplicadores por região. Cuidado: existem duas versões da PROC-042. A mais recente tem multiplicadores mais altos. Na dúvida, use a mais recente (v2), mas se o cliente reclamar do valor, pode ser que o contrato dele ainda esteja na tabela antiga.

### Item 15 — "Cliente diz que é Platinum. Existe esse tier?"
Não existe tier Platinum na NovaTech. Às vezes o cliente confunde com outra transportadora ou com o programa de fidelidade antigo que foi descontinuado em 2022. Oriente que nossos tiers são Gold, Silver e Standard e peça o número do contrato para verificar.

[CHUNK 4]
fonte: FAQ-atendimento.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0199
chunk_index: 3
conteudo: ### Item 22 — "Cliente quer saber sobre seguro de carga. O que falar?"
A NovaTech oferece seguro de carga como adicional. O valor é 0,3% do valor declarado da mercadoria para cargas padrão e 0,8% para cargas perigosas. Detalhe: isso vale para contratos a partir de 2023. Contratos mais antigos podem ter percentuais diferentes — confirme com o Comercial.

### Item 27 — "O tracking mostra 'em trânsito' há 5 dias. O que faço?"
Depende da rota. Rotas para o Norte podem levar até 10 dias úteis. Para Sul/Sudeste, mais de 3 dias parado é estranho. Abra um chamado de rastreamento e classifique como prioridade alta se for Gold ou se o valor da carga for acima de R$ 50.000.

### Item 32 — "Pode enviar carga perigosa com frete expresso?"
Sim, mas precisa de autorização do Compliance e a documentação ANTT tem que estar atualizada. Na prática, demora uns 2 dias para conseguir a autorização, então o 'expresso' acaba não sendo tão expresso. Avise o cliente sobre isso.

[CHUNK 5]
fonte: PROC-042-v2-frete-especial-revisado.md
area: nao-informada
data: nao-informada
versao: nao-informada
score_similaridade: 0.0053
chunk_index: 2
conteudo: ## 3. Prazo de entrega para frete especial

O prazo de entrega para frete especial é calculado como o prazo padrão da rota + 3 dias úteis adicionais para manuseio e roteirização de carga pesada (anteriormente era + 2 dias na versão anterior).

## 4. Condições especiais

- Cargas acima de 5.000kg requerem aprovação prévia do gerente de operações regional.
- Cargas perigosas com peso acima de 500kg seguem tabela específica (PROC-043: Frete de Cargas Perigosas). Nota: a PROC-043 está em processo de revisão pelo Compliance e pode sofrer alterações.
- Descontos de volume: a partir de 8 fretes especiais/mês para o mesmo cliente, aplicar desconto de 5% sobre o multiplicador regional. Acima de 15 fretes/mês, desconto de 10%. Descontos maiores requerem aprovação da Diretoria Comercial.

## 5. Disposições transitórias

Durante o período de transição, chamados abertos antes de 01/12/2023 que ainda estejam em processamento devem usar os multiplicadores da versão anterior (PROC-042 v1). Chamados novos a partir de 01/12/2023 devem usar os multiplicadores desta versão.

```

### Resposta Claude (Haiku 4.5 Extended):

Para carga danificada em trânsito, siga este procedimento:

1. **Orientar o cliente a registrar a ocorrência em até 48h após o recebimento**, incluindo fotos e laudo se possível.
2. **Encaminhar ao time de Sinistros** em sinistros@novatech.com.br com todos os detalhes.
3. A NovaTech investigará e, **se comprovada responsabilidade nossa, reembolsa integralmente** — o cliente não arca com custos.

Este é um caso que sai do atendimento normal e vai para Jurídico, então **não tente resolver na camada de atendimento**.

(Fonte: FAQ de Atendimento, item 38)

**Importante:** Confirme com o time de Sinistros qual a próxima ação antes de prometer prazos ou valores ao cliente.

### Análise:

Retrieval acertou o alvo, e o gerador deu uma resposta fundamentada e bem roteada — mas este é justamente o caso da **armadilha #2** (FAQ como fonte de informação crítica), e vale olhar com lupa porque a aprovação aqui é mais sutil do que parece.

#### Retrieval:

O gabarito diz que para "carga danificada" o único chunk relevante é **FAQ-38**, e que **nenhum documento formal cobre isso**. O FAQ-38 veio em **CHUNK 1, em 1º lugar, com 0.2243** — e o resto despencou (0.0494 para baixo). Recall do obrigatório = 100%, com separação limpa entre o alvo e o ruído. Melhor retrieval da série depois do caso da carga perigosa.

#### Geração:

Tudo na resposta rastreia para o FAQ-38: 48h + fotos/laudo, sinistros@novatech.com.br, investigação + reembolso integral se comprovada responsabilidade, encaminhamento ao Jurídico. **Citação correta** ("FAQ item 38"). Sem alucinação.

Dois acertos finos que merecem nota:

- **Não confundiu danificada com devolução.** O CHUNK 2 (POL-001-D, custos de *devolução*) estava no contexto e era uma isca clássica de conflação — tanto que o próprio FAQ-38 frisa que "carga danificada tem processo *diferente* de devolução". O modelo manteve os dois separados e não misturou as regras de custo de devolução aqui. Boa discriminação.
- **Hedge no lugar certo:** "confirme com Sinistros antes de prometer prazos ou valores" — exatamente onde o excesso de compromisso causaria dano.

#### A ressalva (armadilha #2) — e por que aqui ela é branda

A resposta é uma **procedimento numerado, em tom assertivo, baseado 100% num FAQ informal**, sem nenhum documento formal por trás. Em tese é o gatilho da armadilha #2. Mas há uma diferença crucial em relação ao caso do SLA Gold:

- No **SLA**, o FAQ foi usado como *substituto* de uma tabela contratual que existe e não foi recuperada, e a citação foi *fabricada* apontando para o doc formal. Fonte fraca mascarada de forte → grave.
- Aqui, **não existe documento formal nenhum** sobre carga danificada — o FAQ-38 é a única e melhor fonte disponível. Usá-la não bypassa nada melhor; é o que há. E a citação é honesta ("FAQ").

Então isso é a versão *branda* da armadilha, e o modelo a manejou bem: usou a única fonte existente, citou-a com transparência, e blindou as partes arriscadas (prazos/valores). O único polimento para o padrão-ouro seria uma linha explícita do tipo "essa orientação vem do FAQ interno e não de política formal, então trate como orientação operacional, não como regra contratual" — o hedge final já cobre o risco prático, mas não nomeia a fragilidade de fonte como ele fez com metadados em casos anteriores. Classifico como **PASS com observação de calibração de fonte**, não como falha.

## Síntese da bateria de perguntas (5 casos)

| Caso | Recall | Geração | Veredito |
|---|---|---|---|
| Carga perigosa | 100% | disciplinada | ✅ fundamentado |
| SLA Gold | 0% | alucinou "4h" + citação falsa | ❌ certo por sorte |
| Frete Manaus | 0% | abstenção correta | ✅ falha bem |
| Ramal CEO | sem cobertura | recusa de escopo | ✅ falha bem |
| Carga danificada | 100% | fundamentada, fonte-FAQ honesta | ✅ pass c/ ressalva |

O diagnóstico consolidado é claro e estável ao longo dos cinco: **o gerador é sólido** — descarta ruído, abstém-se quando deve, recusa fora de escopo, cita honestamente — **com uma única fragilidade reprodutível:** quando o retrieval falha *e* há conhecimento paramétrico para preencher (o caso do SLA), ele preenche e mascara com citação. E **o retriever tem um buraco específico em tabelas/dados estruturados** (SLA-2024-B e PROC-042v2-A/B somem do top-k), enquanto recupera bem prosa e FAQ.

Ou seja: as duas correções de maior alavancagem são endurecer o prompt do gerador contra "preencher número sem chunk de suporte" e investigar o chunking/embedding das tabelas — e os scores, que se comportaram de forma consistente e separável nos cinco casos, dão a base para um gate de corte robusto.
