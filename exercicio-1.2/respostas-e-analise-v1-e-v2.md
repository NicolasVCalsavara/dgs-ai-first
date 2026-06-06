## V1:
### 1. "Qual o prazo de devolução para carga perigosa?"

Não existe um "prazo" de devolução para carga perigosa: esse tipo de carga (classes 1 a 6 da ANTT) não é elegível para devolução pelo processo padrão. O cliente deve acionar a Gestão de Riscos (ramal 4500) para tratamento individual.
O prazo de 7 dias úteis vale só para a regra geral, não para carga perigosa. (Fonte: POL-001, seção 3.2.)
Obs: há orientação interna de não tratar como "impossível" e deixar a Gestão de Riscos avaliar exceção caso a caso — mas isso não está na política formal, então não garanta prazo nem elegibilidade ao cliente sem o aval dele

**Análise:** identificou corretamente que o prazo de devolução não se aplica a cargas perigosas, mas a parte sobre não estar na política formal não se encontra nos chunks.

### 2. "Meu cliente é Gold, qual o SLA de resolução?"

Depende do tipo de chamado:

Chamado geral: resolução em até 24h úteis (resposta em até 2h úteis).
Incidente crítico: resolução em até 4h (resposta em até 30min).

Conta como incidente crítico, por exemplo: carga perigosa com irregularidade; carga acima de R$ 100k com status desconhecido há mais de 6h; mais de 5 chamados do mesmo cliente em 24h sobre o mesmo problema. (Fonte: SLA-2024, seções 2 e 3.)
Por ser SLA, confirme no contrato se há exceção vigente antes de comunicar ao cliente.

**Análise:** respondeu corretamente, mas foi desnecessariamente verboso - caso o atendente quisesse saber o que define um incidente como crítico, faria pergunta subsequente.

### 3. "Quanto custa o frete para 600kg para Manaus?"

Não vou calcular o valor — o valor base não consta nos chunks, e o cálculo de frete deve vir da ferramenta determinística, não de mim. Mas os parâmetros fundamentados são:

600kg → frete especial (acima de 500kg), fator de peso 1.0 (faixa 500–1.000kg).
Manaus = Região Norte → multiplicador 1.8 (versão atual).

Atenção ao conflito de versões: a v1 trazia Norte 1.6; a v2 (nov/2023, mais recente) traz 1.8. Pela prioridade de versão, vale 1.8 — mas pela disposição transitória, chamados abertos antes de 01/12/2023 ainda em processamento usam a v1. Confirme qual versão se aplica ao contrato. (Fontes: PROC-042-v2, seções 2 e 2.1; PROC-042 v1, seção 2.1.)
Para o valor final, consulte [ferramenta de cálculo de frete] com destino Manaus, 600kg — ou me peça para acionar a consulta, que eu trago o número oficial com a fonte.

**Análise:** usou um guardrail incorreto. O product specialist informou que: "nunca inventar prazos ou valores que não estejam na documentação". Não há determinação de que deve ser usada a ferramenta de cálculo de frete.

## V2:
### 1. "Qual o prazo de devolução para carga perigosa?"

Carga perigosa (classes 1 a 6 da ANTT — explosivos, gases, líquidos/sólidos inflamáveis, oxidantes, tóxicos/infectantes) não é elegível para devolução pelo processo padrão, então o prazo de 7 dias úteis não se aplica a ela. O caminho é acionar a Gestão de Riscos (ramal 4500) para tratamento individual. (Fonte: POL-001, seção 3.2.)
O FAQ de Atendimento acrescenta que, na prática, casos assim podem receber exceção autorizada pela área de Riscos — então não é "impossível", mas depende de tratamento especial. (Fonte: FAQ-Atendimento, item 3.)
Por envolver exceção a uma regra de elegibilidade, confirme com a Gestão de Riscos antes de orientar o cliente.

**Análise:** ateve-se aos chunks de forma mais precisa que antes.

### 2. "Meu cliente é Gold, qual o SLA de resolução?"

Para Gold, a resolução é de até 24h úteis em chamado geral e até 4h em incidente crítico. (Fonte: SLA-2024, seção 2.) Posso detalhar o que conta como incidente crítico, se precisar.
Por ser SLA, valide no contrato se há exceção vigente antes de comunicar ao cliente.

**Análise:** melhora considerável de verbosidade.

### 3. "Quanto custa o frete para 600kg para Manaus?"

Não consigo fechar o valor: a documentação traz o multiplicador (Norte 1.8) e o fator de peso (1.0, faixa 500–1.000kg), mas não traz o valor base — e eu não invento a parte que falta. (Fonte: PROC-042-v2, seções 2 e 2.1.)
Dois pontos sobre o multiplicador, caso precise: prevalece a versão mais recente (Norte 1.8, PROC-042-v2, novembro/2023), e não a antiga (Norte 1.6, PROC-042 v1); mas há disposição transitória — chamados abertos antes de 01/12/2023 ainda em processamento seguem a tabela antiga. (Fonte: PROC-042-v2, seção 5.)
Por ser frete, confirme o valor final com o canal responsável antes de comunicar ao cliente.

**Análise:** não teve mais a alucinação de guardrail.
