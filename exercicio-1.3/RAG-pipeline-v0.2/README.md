# Pipeline RAG minimo - NovaTech

Este projeto implementa um pipeline RAG minimo com 3 etapas:

1. Ingestao dos documentos da pasta `DocumentacaoNovaTech`.
2. Busca vetorial no ChromaDB com score de similaridade.
3. Montagem do prompt completo (system prompt + chunks + pergunta).

## Stack adotada

- LangChain (splitter, embeddings e vector store wrappers)
- ChromaDB (persistencia vetorial via `langchain-chroma`)
- sentence-transformers com modelo `all-MiniLM-L6-v2` (via `langchain-huggingface`)

## Estrategia de chunking (e justificativa)

- Tipo: `RecursiveCharacterTextSplitter` com separadores estruturais.
- Configuracao: `chunk_size=1200`, `chunk_overlap=180`.
- Separadores: titulos (`##`, `###`), paragrafos e sentencas.

Justificativa:

- Os documentos sao majoritariamente Markdown com secoes e tabelas.
- O splitter primeiro tenta quebrar por fronteiras semanticas (titulos/paragrafos), reduzindo cortes no meio de regras.
- O overlap de 180 caracteres preserva contexto de borda, evitando perda de termos relevantes na busca.
- O tamanho de 1200 caracteres equilibra granularidade de retrieval e contexto suficiente para respostas factuais.

## Requisitos

Instale dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Uso

### 1) Ingestao

```powershell
python rag_pipeline.py ingest
```

Isso:

- Le os `.md` de `DocumentacaoNovaTech`.
- Divide em chunks.
- Gera embeddings com `all-MiniLM-L6-v2`.
- Persiste no ChromaDB local em `.chroma`.

### 2) Busca + montagem de prompt

```powershell
python rag_pipeline.py ask "Qual o SLA para cliente Gold em incidente critico?" --top-k 5
```

Isso:

- Gera embedding da pergunta.
- Recupera os `N` chunks mais similares no ChromaDB.
- Exibe fonte, chunk e score de similaridade.
- Monta o prompt completo e salva em `prompt_montado.txt`.

## Estrutura

- `rag_pipeline.py`: implementacao das funcoes principais.
- `system-prompt-assistente-novatech-v2.md`: system prompt usado na montagem.
- `DocumentacaoNovaTech/`: base de documentos do Anexo A.
