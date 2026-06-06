from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

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
    # Strategy: preserve semantic boundaries first (headings/paragraphs), with overlap
    # to reduce boundary loss in retrieval when terms sit near chunk edges.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=180,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )

    chunked_docs: List[Dict[str, str]] = []
    for doc in documents:
        chunks = splitter.split_text(doc["content"])
        for index, chunk in enumerate(chunks, start=1):
            chunked_docs.append(
                {
                    "id": f"{doc['source']}::chunk-{index}",
                    "source": doc["source"],
                    "chunk_index": str(index),
                    "content": chunk.strip(),
                }
            )
    return chunked_docs


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
) -> List[RetrievedChunk]:
    vector_store = get_vector_store(chroma_dir=chroma_dir, collection_name=collection_name)
    retrieved = vector_store.similarity_search_with_score(question, k=n_results)

    results: List[RetrievedChunk] = []
    for doc, distance in retrieved:
        metadata = doc.metadata or {}
        similarity = 1.0 - float(distance)
        results.append(
            RetrievedChunk(
                chunk_id=metadata.get("original_chunk_id", "desconhecido"),
                content=doc.page_content,
                metadata=metadata,
                distance=float(distance),
                similarity_score=similarity,
            )
        )
    return results


def build_prompt(
    question: str,
    retrieved_chunks: List[RetrievedChunk],
    system_prompt_path: Path = DEFAULT_SYSTEM_PROMPT_PATH,
) -> str:
    system_prompt = system_prompt_path.read_text(encoding="utf-8").strip()

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

    return (
        f"{system_prompt}\n\n"
        "---\n"
        "## CONTEXTO RECUPERADO\n"
        "---\n"
        f"{'\n\n'.join(chunks_block)}\n\n"
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
    ask_parser.add_argument("--top-k", type=int, default=5)
    ask_parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    ask_parser.add_argument("--chroma-dir", type=Path, default=DEFAULT_CHROMA_DIR)
    ask_parser.add_argument("--collection", type=str, default=DEFAULT_COLLECTION)
    ask_parser.add_argument(
        "--system-prompt",
        type=Path,
        default=DEFAULT_SYSTEM_PROMPT_PATH,
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
