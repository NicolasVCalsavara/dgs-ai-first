# Estrutura de Contexto do Prompt — Assistente NovaTech

Mapa do que entra em **cada chamada** ao GPT-4o, separando o que é **estático** (idêntico em toda query) do que é **dinâmico** (muda por query), com estimativa de tokens.

> **Sobre os números.** São **estimativas** para português + tokenizer `o200k_base` (GPT-4o), obtidas medindo o prompt real e combinando duas contagens (caracteres ÷ 3,6 e palavras × 1,5). Não foi possível rodar o tokenizer exato neste ambiente (download do vocabulário bloqueado pela rede). Margem esperada: **~±15%**. Para fechar o número, rodar `tiktoken` com `o200k_base` num ambiente com acesso, ou medir sobre tráfego real.

---

## 1. Anatomia de uma chamada

```
┌─ ESTÁTICO (cacheável — vai em toda query) ─────────────┐
│ System prompt: Seções 1–8                              │  ~2,8K tokens
├─ DINÂMICO (muda por query) ────────────────────────────┤
│ Histórico de conversa (cresce no chamado)              │  0–1,2K
│ [RESULTADO_TOOL] frete/SLA (quando há)                 │  0–0,3K
│ [CHUNK]s recuperados (5–10, top-rankeados)             │  2,7K–8,4K
│ Query do atendente                                     │  ~0,04K
├─ RESERVA DE SAÍDA ──────────────────────────────────────┤
│ Resposta gerada (fundamentada + citação)               │  0,4K–1,0K
└─────────────────────────────────────────────────────────┘
Janela GPT-4o: 128K  →  uso típico ~9K (≈7%)
```

---

## 2. Parte estática (system prompt — toda query)

É o prompt que geramos (Seções 1–8), **idêntico em todas as chamadas**. A nota de produção é removida no deploy e não conta.

| Seção do prompt | Conteúdo | Tokens (est.) |
|---|---|---|
| Cabeçalho | Título | ~20 |
| 1. Identidade e propósito | Quem é, para quem, princípio nuclear | ~250 |
| 2. Princípios fundamentais | Os 5 inegociáveis | ~215 |
| 3. Regras e guardrails | Grounding, cálculo, abstenção, citação, LGPD, escopo, confidencialidade | ~700 |
| 4. Ordem de prioridade em conflito | Os 4 níveis de desempate | ~330 |
| 5. Como usar chunks/tools | **Instruções + template** do formato (não o conteúdo) | ~265 |
| 6. Formato de resposta | Idioma, tom, estrutura, tamanho | ~220 |
| 7. Mensagens padrão | Abstenção, fora de escopo, conflito, sem-tool | ~250 |
| 8. Exemplos (few-shot) | 5 exemplos A–E | ~520 |
| **Total estático** | | **~2,8K** (faixa ~2,5K–3,1K) |

**Observações:**
- As duas maiores fatias são **Regras (Seção 3, ~700)** e **Exemplos (Seção 8, ~520)** — juntas, ~44% do estático.
- A **Seção 5 é mista**: as *instruções e o template* (`[CHUNK n] fonte/área/data/versão...`) são estáticos; o **conteúdo preenchido** dos chunks é dinâmico (entra na Parte 3).

---

## 3. Parte dinâmica (muda a cada query)

| Componente | O que é | Tokens (est.) | Observação |
|---|---|---|---|
| **Chunks recuperados** | 5–10 trechos top-rankeados, cada um ~500–800 tokens + wrapper de metadados (~35) | **2,7K–8,4K** (central ~4,8K) | **Maior componente dinâmico.** É o que realmente preenche a janela. |
| **Histórico de conversa** | Turnos anteriores do chamado; cresce ao longo da conversa | **0–1,2K** | 0 no 1º turno. Truncar/resumir para não invadir a "zona morta" central (lost-in-the-middle). |
| **Resultado de tool** | `[RESULTADO_TOOL]` de frete/SLA, quando aplicável | **0–0,3K** | Ausente em perguntas procedimentais; ~80–200 por resultado. |
| **Query do atendente** | A pergunta em si | **~20–60** | Curta e factual, por design. |
| **Reserva de saída** | A resposta gerada (não é entrada, mas consome a janela) | **0,4K–1,0K** | Resposta fundamentada + citação é curta; conflito gasta um pouco mais. |

---

## 4. Orçamento por query (estático + dinâmico + saída)

| Cenário | Estático | Histórico | Tool | Chunks | Query | Saída | **Total** | % de 128K |
|---|---|---|---|---|---|---|---|---|
| **Leve** (início de conversa, poucos chunks, sem tool) | 2,8K | 0 | 0 | 2,7K | 0,04K | 0,5K | **~6K** | ~5% |
| **Típico** (7 chunks, com tool, algum histórico) | 2,8K | 0,6K | 0,15K | 4,8K | 0,04K | 0,7K | **~9K** | ~7% |
| **Pesado** (fim de chamado longo, 10 chunks, histórico cheio) | 2,8K | 1,2K | 0,3K | 8,4K | 0,06K | 1,0K | **~14K** | ~11% |

Mesmo no cenário pesado, usa-se **~11% da janela**. Sobra deliberada — coerente com a Seção 4 da análise de viabilidade: **o orçamento de contexto não é o gargalo; a relevância da recuperação é.** Encher o restante com mais chunks pioraria a qualidade (lost-in-the-middle), não melhoraria.

---

## 5. Implicações para o protótipo

**O estático ficou em ~2,8K, não nos ~2K assumidos na Seção 4 da viabilidade.** A diferença vem dos guardrails (Seção 3) e dos exemplos (Seção 8) que adicionamos. Em termos de *janela*, é irrelevante (continua ínfimo perto de 128K). Em termos de *custo/latência*, importa: esse bloco é pago em **toda** query (~190/dia).

**Recomendação 1 — Prompt caching.** Como o estático é um prefixo fixo e repetido, habilitar *prompt caching* (suportado no Azure OpenAI) corta custo e latência do bloco de ~2,8K em cada chamada. Para isso, **montar a chamada com o estático como prefixo estável** e o conteúdo dinâmico **depois** dele (chunks, histórico, query). Não intercalar dinâmico no meio do estático, ou o cache não aproveita.

**Recomendação 2 — Ordem de montagem (lost-in-the-middle).**
1. System prompt estático (prefixo cacheável).
2. Histórico resumido/truncado.
3. Bloco de chunks — com os de **maior score no início e no fim** do bloco, e os de menor confiança no meio.
4. Query do atendente por último (mais recente).

**Recomendação 3 — Alavanca de corte (se um dia precisar).** Se o estático crescer e incomodar custo, a fatia mais segura de enxugar é a **Seção 8 (exemplos)** — reduzir de 5 para 2–3 cobre os casos críticos (abstenção, conflito, não-calcular) por ~250 tokens. Hoje **não é necessário**: o headroom é enorme e os exemplos melhoram a qualidade.

**Recomendação 4 — Medir de verdade.** Estes valores são estimativas (PT + o200k, sem o tokenizer exato disponível aqui). Antes de fechar o modelo de custo (Seção 10 da viabilidade), rodar `tiktoken`/`o200k_base` sobre o prompt real e sobre uma amostra de chunks reais — fecha de uma vez a incerteza de tokens que vinha sendo arrastada desde o dimensionamento da base.
