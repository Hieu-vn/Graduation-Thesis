"""
Embeddings Service - SentenceTransformer + ChromaDB Integration
"""
import logging
from typing import List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from app.core.config import settings

logger = logging.getLogger(__name__)

_embedding_model: Optional[SentenceTransformer] = None
_chroma_client: Optional[chromadb.PersistentClient] = None


def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("Embedding model loaded successfully")
    return _embedding_model


def get_chroma_client() -> chromadb.PersistentClient:
    global _chroma_client
    if _chroma_client is None:
        logger.info(f"Initializing Chroma at: {settings.CHROMA_PERSIST_DIR}")
        _chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        logger.info("Chroma client initialized")
    return _chroma_client


def get_user_collection(user_id: str) -> chromadb.Collection:
    client = get_chroma_client()
    collection_name = f"user_{user_id.replace('-', '_')}"
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def embed_text(text: str) -> List[float]:
    model = get_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embed_transactions(user_id: str, transactions: list) -> int:
    if not transactions:
        return 0

    collection = get_user_collection(user_id)
    model = get_embedding_model()

    documents = []
    metadatas = []
    ids = []

    for t in transactions:
        text = f"{t.description}"
        if t.notes:
            text += f" - {t.notes}"

        documents.append(text)
        metadatas.append({
            "transaction_id": t.id,
            "type": t.type,
            "amount": float(t.amount),
            "currency": t.currency,
            "date": str(t.date),
            "category_id": t.category_id or "",
            "account_id": t.account_id,
        })
        ids.append(t.id)

    raw_embeddings = model.encode(documents, normalize_embeddings=True)
    embeddings = [emb.tolist() for emb in raw_embeddings]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    logger.info(f"Embedded {len(transactions)} transactions for user {user_id}")
    return len(transactions)


def semantic_search(user_id: str, query: str, top_k: int = 5) -> List[dict]:
    collection = get_user_collection(user_id)

    if collection.count() == 0:
        return []

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    matches = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            matches.append({
                "document": doc,
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else 0,
            })

    return matches
