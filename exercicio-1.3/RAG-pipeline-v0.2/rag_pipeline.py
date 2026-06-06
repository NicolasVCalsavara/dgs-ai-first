from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import re

import chromadb
from chromadb.errors import NotFoundError
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_DOCS_DIR = Path("DocumentacaoNovaTech")
DEFAULT_SYSTEM_PROMPT_PATH = Path("system-prompt-assistente-novatech-v2.md")
DEFAULT_CHROMA_DIR = Path(".chroma")
DEFAULT_COLLECTION = "novatech_kb"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.0


@dataclass
class RetrievedChunk:
    chunk_id: str
    content: str
    metadata: Dict[str, str]
    distance: float
    similarity_score: float


def read_markdown_documents(docs_dir: Path) -> List[Dict[str, str]]:
    docs: List[Dict[str, str]] = []
    for file_path in sorted(docs_dir.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")
        docs.append(
            {
                "source": file_path.name,
                "content": text,
            }
        )
    return docs


def split_documents(documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # Chunk de 800 chars: granular o suficiente para separar FAQ items individuais,
    # mas grande o bastante para manter cabeçalho de seção junto com a tabela/conteúdo.
    # Overlap de 100 chars mantém contexto de borda.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )

    chunked_docs: List[Dict[str, str]] = []
    for doc in documents:
        chunks = splitter.split_text(doc["content"])
        enriched = _enrich_chunks_with_headings(doc["content"], chunks)
        for index, chunk in enumerate(enriched, start=1):
            chunked_docs.append(
                {
                    "id": f"{doc['source']}::chunk-{index}",
                    "source": doc["source"],
                    "chunk_index": str(index),
                    "content": chunk.strip(),
                }
            )
    return chunked_docs


def _enrich_chunks_with_headings(full_text: str, chunks: List[str]) -> List[str]:
    """Prepend the last section heading to chunks that lost it during splitting.

    When RecursiveCharacterTextSplitter splits on '## ' or '### ', the heading
    goes to the previous chunk and the content starts without context. This
    reattaches the heading so embeddings include "## 2. Tabela de SLAs" along
    with the table data, improving retrieval of structured content.
    """
    headings = re.findall(r"^(#{1,3} .+)$", full_text, re.MULTILINE)
    if not headings:
        return chunks

    enriched: List[str] = []
    for chunk in chunks:
        # If chunk already starts with a heading, keep it as-is
        if re.match(r"^#{1,3} ", chunk):
            enriched.append(chunk)
            continue

        # Find the last heading that appears in the full text BEFORE this chunk
        chunk_start = full_text.find(chunk[:80])
        if chunk_start == -1:
            enriched.append(chunk)
            continue

        last_heading = None
        for h in headings:
            h_pos = full_text.find(h)
            if h_pos < chunk_start:
                last_heading = h
            else:
                break

        if last_heading and last_heading not in chunk:
            enriched.append(f"[Seção: {last_heading}]\n{chunk}")
        else:
            enriched.append(chunk)

    return enriched


def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vector_store(
    chroma_dir: Path = DEFAULT_CHROMA_DIR,
    collection_name: str = DEFAULT_COLLECTION,
) -> Chroma:
    embeddings = get_embedding_model()
    return Chroma(
        collection_name=collection_name,
        persist_directory=str(chroma_dir),
        embedding_function=embeddings,
    )


def ingest_documents(
    docs_dir: Path = DEFAULT_DOCS_DIR,
    chroma_dir: Path = DEFAULT_CHROMA_DIR,
    collection_name: str = DEFAULT_COLLECTION,
) -> None:
    documents = read_markdown_documents(docs_dir)
    if not documents:
        raise ValueError(f"Nenhum .md encontrado em: {docs_dir}")

    chunks = split_documents(documents)
    chunk_docs = [
        Document(
            page_content=c["content"],
            metadata={
                "source": c["source"],
                "chunk_index": c["chunk_index"],
                "original_chunk_id": c["id"],
            },
        )
        for c in chunks
    ]

    client = chromadb.PersistentClient(path=str(chroma_dir))
    try:
        client.delete_collection(collection_name)
    except NotFoundError:
        pass

    vector_store = get_vector_store(chroma_dir=chroma_dir, collection_name=collection_name)
    vector_store.add_documents(chunk_docs)

    indexed_count = len(vector_store.get(include=[]).get("ids", []))
    print(
        f"Ingestao concluida. Documentos: {len(documents)} | Chunks: {len(chunks)} | "
        f"Collection: {collection_name} | Indexados: {indexed_count}"
    )


def search_chunks(
    question: str,
    n_results: int = 5,
    chroma_dir: Path = DEFAULT_CHROMA_DIR,
    collection_name: str = DEFAULT_COLLECTION,
    threshold: float = SIMILARITY_THRESHOLD,
    max_per_source: int = 3,
) -> List[RetrievedChunk]:
    vector_store = get_vector_store(chroma_dir=chroma_dir, collection_name=collection_name)
    # Busca janela maior para depois filtrar por threshold e diversificar fontes
    fetch_k = max(n_results * 3, 15)
    retrieved = vector_store.similarity_search_with_score(question, k=fetch_k)

    # Reserva ~30% dos slots para vizinhos
    initial_cap = max(n_results - 3, 3)
    results: List[RetrievedChunk] = []
    source_count: Dict[str, int] = {}
    for doc, distance in retrieved:
        metadata = doc.metadata or {}
        similarity = 1.0 - float(distance)
        if similarity < threshold:
            continue
        source = metadata.get("source", "")
        if source_count.get(source, 0) >= max_per_source:
            continue
        source_count[source] = source_count.get(source, 0) + 1
        results.append(
            RetrievedChunk(
                chunk_id=metadata.get("original_chunk_id", "desconhecido"),
                content=doc.page_content,
                metadata=metadata,
                distance=float(distance),
                similarity_score=similarity,
            )
        )
        if len(results) >= initial_cap:
            break

    # Expansão por vizinhança: para cada chunk recuperado, busca chunks adjacentes
    # do mesmo documento (±1 index). Isso compensa embeddings fracos em tabelas e
    # dados estruturados — se um cabeçalho de seção é recuperado, o conteúdo da
    # seção (ex.: tabela de SLAs) vem junto.
    results = _expand_with_neighbors(results, vector_store, n_results)
    return results


def _expand_with_neighbors(
    results: List[RetrievedChunk],
    vector_store: Chroma,
    max_total: int,
) -> List[RetrievedChunk]:
    if not results:
        return results

    seen_ids = {r.chunk_id for r in results}
    # Coleta vizinhos com o score do pai para ordenação
    neighbor_requests: List[tuple] = []  # (parent_score, neighbor_id)

    for r in results:
        source = r.metadata.get("source", "")
        parent_score = r.similarity_score
        try:
            idx = int(r.metadata.get("chunk_index", "0"))
        except ValueError:
            continue
        for neighbor_idx in [idx - 1, idx + 1]:
            if neighbor_idx < 1:
                continue
            neighbor_id = f"{source}::chunk-{neighbor_idx}"
            if neighbor_id not in seen_ids:
                neighbor_requests.append((parent_score, neighbor_id))
                seen_ids.add(neighbor_id)

    if not neighbor_requests:
        return results

    # Ordena vizinhos pelo score do pai (mais relevante primeiro)
    neighbor_requests.sort(key=lambda x: x[0], reverse=True)
    neighbor_ids_to_find = [nid for _, nid in neighbor_requests]

    all_data = vector_store.get(
        ids=None,
        include=["documents", "metadatas"],
    )
    id_to_doc = {}
    for doc_id, doc_text, meta in zip(
        all_data.get("ids", []),
        all_data.get("documents", []),
        all_data.get("metadatas", []),
    ):
        orig_id = (meta or {}).get("original_chunk_id", "")
        if orig_id in neighbor_ids_to_find:
            id_to_doc[orig_id] = (doc_text, meta)

    neighbors: List[RetrievedChunk] = []
    for nid in neighbor_ids_to_find:
        if nid in id_to_doc:
            doc_text, meta = id_to_doc[nid]
            neighbors.append(
                RetrievedChunk(
                    chunk_id=nid,
                    content=doc_text,
                    metadata=meta or {},
                    distance=-1.0,
                    similarity_score=-1.0,
                )
            )

    combined = results + neighbors
    return combined[:max_total]


def build_prompt(
    question: str,
    retrieved_chunks: List[RetrievedChunk],
    system_prompt_path: Path = DEFAULT_SYSTEM_PROMPT_PATH,
) -> str:
    system_prompt = system_prompt_path.read_text(encoding="utf-8").strip()

    # Sinal de confiança do retrieval para o LLM
    if not retrieved_chunks:
        confidence = "NENHUM"
        confidence_note = (
            "Nenhum chunk passou o limiar de similaridade. "
            "A base de conhecimento provavelmente não cobre esta pergunta. "
            "Siga o procedimento de abstenção (Seção 3.3)."
        )
    else:
        max_score = max(c.similarity_score for c in retrieved_chunks)
        if max_score >= 0.25:
            confidence = "ALTO"
            confidence_note = "Pelo menos um chunk tem boa relevância."
        elif max_score >= 0.10:
            confidence = "MEDIO"
            confidence_note = (
                "Os chunks recuperados têm similaridade moderada. "
                "Avalie com cuidado se realmente sustentam a resposta."
            )
        else:
            confidence = "BAIXO"
            confidence_note = (
                "Todos os chunks têm similaridade muito baixa. "
                "Provavelmente não cobrem a pergunta. "
                "Prefira abstenção a menos que encontre uma resposta clara no conteúdo."
            )

    chunks_block: List[str] = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk.metadata.get("source", "desconhecida")
        chunk_index = chunk.metadata.get("chunk_index", "?")
        chunks_block.append(
            "\n".join(
                [
                    f"[CHUNK {i}]",
                    f"fonte: {source}",
                    "area: nao-informada",
                    "data: nao-informada",
                    "versao: nao-informada",
                    f"score_similaridade: {chunk.similarity_score:.4f}",
                    f"chunk_index: {chunk_index}",
                    f"conteudo: {chunk.content}",
                ]
            )
        )

    retrieval_header = (
        f"Confianca do retrieval: {confidence}\n"
        f"Nota: {confidence_note}\n"
        f"Chunks recuperados: {len(retrieved_chunks)}"
    )

    return (
        f"{system_prompt}\n\n"
        "---\n"
        "## CONTEXTO RECUPERADO\n"
        "---\n"
        f"{retrieval_header}\n\n"
        f"{chr(10).join(f'{chr(10)}{b}' for b in chunks_block)}\n\n"
        "---\n"
        "## PERGUNTA DO ATENDENTE\n"
        "---\n"
        f"{question}\n"
    )


def print_search_results(results: List[RetrievedChunk]) -> None:
    for i, item in enumerate(results, start=1):
        preview = item.content.replace("\n", " ").strip()
        if len(preview) > 220:
            preview = preview[:220] + "..."

        source = item.metadata.get("source", "desconhecida")
        print(
            f"[{i}] fonte={source} | chunk={item.metadata.get('chunk_index', '?')} "
            f"| score={item.similarity_score:.4f} | distance={item.distance:.4f}"
        )
        print(f"    {preview}")


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Pipeline RAG minimo para NovaTech")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Ingerir documentos no ChromaDB")
    ingest_parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    ingest_parser.add_argument("--chroma-dir", type=Path, default=DEFAULT_CHROMA_DIR)
    ingest_parser.add_argument("--collection", type=str, default=DEFAULT_COLLECTION)

    ask_parser = subparsers.add_parser("ask", help="Buscar chunks e montar prompt")
    ask_parser.add_argument("question", type=str)
    ask_parser.add_argument("--top-k", type=int, default=8)
    ask_parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    ask_parser.add_argument("--chroma-dir", type=Path, default=DEFAULT_CHROMA_DIR)
    ask_parser.add_argument("--collection", type=str, default=DEFAULT_COLLECTION)
    ask_parser.add_argument(
        "--system-prompt",
        type=Path,
        default=DEFAULT_SYSTEM_PROMPT_PATH,
    )
    ask_parser.add_argument(
        "--threshold",
        type=float,
        default=SIMILARITY_THRESHOLD,
        help="Score minimo de similaridade para incluir um chunk (default: 0.0)",
    )

    args = parser.parse_args()

    if args.command == "ingest":
        ingest_documents(
            docs_dir=args.docs_dir,
            chroma_dir=args.chroma_dir,
            collection_name=args.collection,
        )
        return

    if args.command == "ask":
        results = search_chunks(
            question=args.question,
            n_results=args.top_k,
            chroma_dir=args.chroma_dir,
            collection_name=args.collection,
            threshold=args.threshold,
        )
        print("Chunks recuperados:")
        print_search_results(results)

        prompt = build_prompt(
            question=args.question,
            retrieved_chunks=results,
            system_prompt_path=args.system_prompt,
        )

        output_path = Path("prompt_montado.txt")
        output_path.write_text(prompt, encoding="utf-8")
        print(f"\nPrompt completo salvo em: {output_path}")


if __name__ == "__main__":
    run_cli()
