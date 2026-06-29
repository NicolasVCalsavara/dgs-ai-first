**1. (Bloqueante, e arrastado das duas revisões anteriores) `url` obrigatória rejeita toda resposta fiel ao corpus.** A decisão #3 continua intacta — e segue invertendo a sua ordem de prioridade (escolheu o código sobre a doc). Testei: uma resposta citando `POL-001-B` sem URL **falha** o schema (`passa SEM url? false`). Como o corpus nunca tem URL, o resultado é que *toda* resposta real cai na fallback, ou o serviço inventa uma URL pra passar — exatamente a alucinação que o guardrail existe pra impedir. De quebra, a própria fallback fabrica uma (`https://novatech.example/human-handoff`). Esse é o defeito de raiz e está no `types.ts`, mas o validator é onde ele vira dano.

**2. (Grave) O guardrail 2 é fail-open e vaza em variações triviais.** A lógica exige carga perigosa + devolução + afirmação **no mesmo segmento de frase**, e só bloqueia se casar o regex de afirmação. Resultado dos testes: das 6 frases, **4 que deveriam bloquear passaram**:

- "Sobre devolução de carga perigosa: sim, é permitido." → a afirmação está na 2ª frase, o assunto na 1ª; o split por `.!?;` separa as duas e nenhum segmento tem tudo. Passou.
- "A carga perigosa pode, conforme análise do gerente, ser devolvida." → "pode" e "devolvida" ficam a mais de 20 caracteres de distância; a janela `.{0,20}` não alcança. Passou.
- "A devolução de carga perigosa depende de avaliação." → não afirma explicitamente, mas também **não contém a negativa obrigatória**. O guardrail 2 dizia "DEVEM conter a negativa" — uma resposta vaga sobre o tema sem a negativa deveria bloquear, e passou.
- "Mercadoria perigosa pode ser devolvida normalmente." → "mercadoria perigosa" não está no regex (só "carga" e "produto"); sinônimo trivial escapa.

A raiz é a postura: um guardrail determinístico que protege uma negativa regulatória deveria **fail-safe** (bloquear quando não tem certeza), e este faz o oposto — só bloqueia no encaixe estreito do regex de afirmação, deixando passar tudo que não casa. O comentário de "limitação" é honesto, mas subestima: não são só "formulações indiretas", são frases diretas em duas orações.

**3. (Médio — o palpite do enunciado) O schema aceita campos extras.** `z.object` sem `.strict()` aceita e **descarta silenciosamente** chaves desconhecidas: testei com `campo_injetado` e o parse deu `success: true`, removendo o campo sem avisar. Para um harness de saída de formato fixo, um output adulterado/inesperado deveria ser rejeitado e logado, não silenciosamente limpo. Falta `.strict()`.

**Menores, que eu anotaria:**

A anotação `z.ZodType<SourceDocument>` no `SourceDocumentSchema` é um tiro no pé que já tínhamos sinalizado: desliga parte da inferência e mascara drift entre schema e tipo. Não é o idioma do `validator.ts`.

O `validateStructuredResponse` constrói um `ValidationError` só para extrair `.name`/`.message`/`.details` e logar — ele nunca é lançado. É objeto criado à toa; daria pra logar a razão direto.

Sobre o **logger**: funcional, mas é um `console.error(JSON)` com nível fixo `"error"` — o `error-handling`/`logging-observability` pedia níveis e `requestId` de correlação, que não existem aqui. E todo evento sai como `error`, inclusive coisas que talvez fossem `warn`. Aceitável como stub mínimo, mas não é o logger estruturado que a Foundation descreve — vale marcar que ele ainda não atende àquela skill.

Resumindo: o `safeParse` e a separação estrutural/conteúdo estão no caminho certo, mas o guardrail 2 hoje protege pouco (fail-open + janela curta + split de frase + sinônimo faltando), o schema deixa passar campo extra, e o `url` obrigatório continua sabotando o propósito inteiro. Quando você quiser, corrijo os três — a mudança central no guardrail 2 é inverter para "bloqueia se o tema aparece e a negativa **não** está presente".