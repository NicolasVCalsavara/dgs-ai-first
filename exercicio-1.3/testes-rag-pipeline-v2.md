## Alterações no Pipeline (`rag_pipeline.py`)

**1. Chunk size: 1200 → 800 chars** — FAQ items que vinham bundled (38+41+45 num chunk só) agora são separados, melhorando a granularidade do retrieval. De ~15 chunks para 24.

**2. Enrichment de headings** — Chunks que perderam o cabeçalho de seção durante o split ganham um prefixo `[Seção: ## X]`. Isso melhora o embedding de conteúdo estruturado (tabelas) que perde contexto semântico sem o título.

**3. Threshold de similaridade** (gate) — Chunks com `score < 0.0` são filtrados. Para a query "ramal do CEO" (fora de escopo), retorna 0 chunks em vez de 5 irrelevantes. Configurável via `--threshold`.

**4. Sinal de confiança do retrieval** — O prompt montado agora inclui `Confianca do retrieval: ALTO|MEDIO|BAIXO|NENHUM` com nota explicativa. Dá ao LLM um sinal calibrado para decidir entre responder e abster-se.

**5. Expansão por vizinhança** — Busca chunks adjacentes (±1 index) dos chunks recuperados. Compensa embeddings fracos em dados tabulares — se um chunk de "penalidades SLA" é recuperado, a "definição de incidente crítico" (chunk vizinho) vem junto.

**6. Diversificação de fontes** — Máximo 3 chunks por documento na busca inicial, evitando que FAQ monopolize todos os slots.

## Alterações no System Prompt (`system-prompt-assistente-novatech-v2.md`)

**7. Princípio 7 (novo)**: "Cada número/valor citado deve ser rastreável a um chunk específico" — ataca diretamente o caso do SLA Gold onde o "4h" foi alucinado.

**8. Princípio 8 (novo)**: "Nunca atribua informação a uma fonte que não a contém" — ataca a citação fabricada (metadados de SLA-2024 usados para credibilizar um número que veio do FAQ).

**9. Regra de rastreabilidade na citação (3.4)** — Reforço: a fonte citada deve ser o chunk que contém literalmente o dado.

**10. Seção 3.9 (nova)**: Como interpretar o sinal de confiança do retrieval (NENHUM → abstenção; BAIXO → preferir abstenção; etc.).

**11. Exemplo E atualizado**: Inclui nota interna explicando que ambos os valores devem aparecer literalmente no chunk.

**12. Exemplo G (novo)**: Demonstra o anti-padrão do teste 2 — dado parcial no contexto, LLM deve informar o que tem e abster-se do que falta, sem completar com conhecimento paramétrico.

## Pergunta 1
Qual o prazo de devolução para carga perigosa?

### Resposta Claude (Haiku 4.5 Extended):

Não encontrei na documentação oficial uma resposta segura para isso. 

O que consta é que devoluções em geral têm prazo de **7 dias úteis** (a partir do recebimento) — após isso, não são elegíveis para devolução padrão. (Fonte: POL-001, seção 3.5.) Porém, a documentação menciona que cargas perigosas seguem procedimentos específicos (PROC-043), e essa PROC não foi recuperada nos trechos que tenho.

Como a PROC-043 está em revisão pelo Compliance e pode ter prazos diferentes, confirme com a **área de Compliance** ou o **Comercial** antes de garantir ao cliente.

## Pergunta 2
Meu cliente é Gold, qual o SLA de resolução?

### Resposta Claude (Haiku 4.5 Extended):

Para Gold, a resolução é **até 24 horas**. (Fonte: FAQ-atendimento, Item 41.)

Para incidentes críticos, os prazos são menores, mas a documentação recuperada não traz o tempo específico — confirme direto na tabela SLA-2024 ou com o Comercial se precisar.

Por ser SLA, valide no contrato do cliente antes de comunicar.

## Pergunta 3
Quanto custa o frete para 600kg para Manaus?

### Resposta Claude (Haiku 4.5 Extended):

Não consigo fechar o valor: a documentação traz o **fator de peso (1.0 para 600kg)** e o **multiplicador regional para Norte (1.6)**, mas **não traz o valor base** — que é a tarifa publicada na tabela mensal de fretes.

A fórmula é: Valor do frete = Valor base × 1.6 × 1.0. Faltando o valor base, eu não invento esse número.

(Fonte: PROC-042-frete-especial-v1, seção 2 e 2.1.)

**Nota:** existem duas versões de PROC-042 em vigência (v1 e v2); em caso de dúvida sobre qual multiplicador usar, confirme com o Comercial.

Para o valor final, confirme com a **área Comercial ou Operações**. Por ser frete, valide antes de comunicar ao cliente.

## Pergunta 4
Qual o ramal do CEO?

### Resposta Claude (Haiku 4.5 Extended):

Eu ajudo apenas com a documentação e os procedimentos de atendimento da NovaTech (frete, SLA, devoluções e processos). Para isso aí, melhor usar outro canal.

## Pergunta 5
A carga do cliente foi danificada. Como proceder?

### Resposta Claude (Haiku 4.5 Extended):

Carga danificada em trânsito segue um processo **diferente de devolução**:

1. **O cliente registra a ocorrência em até 48h** após o recebimento, com fotos e laudo se possível.
2. **A NovaTech investiga.** Se comprovada responsabilidade nossa, reembolsamos integralmente.
3. **Encaminhe o caso para sinistros@novatech.com.br** — isso passa pelo Jurídico, não pelo atendimento normal.

(Fonte: FAQ de Atendimento, item 38.)