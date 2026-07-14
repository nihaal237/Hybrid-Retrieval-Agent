import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer
from . import config


class VectorMemoryStore:
    def __init__(self):
        self.client = QdrantClient(path=config.QDRANT_PATH)
        self.embedder = SentenceTransformer(config.EMBEDDING_MODEL)
        self._ensure_collection()

    def _ensure_collection(self):
        names = [c.name for c in self.client.get_collections().collections]
        if config.QDRANT_COLLECTION not in names:
            self.client.create_collection(
                collection_name=config.QDRANT_COLLECTION,
                vectors_config=qmodels.VectorParams(
                    size=config.EMBEDDING_DIM,
                    distance=qmodels.Distance.COSINE,
                ),
            )

    def add_memory(self, text: str, metadata: dict = None) -> str:
        mem_id = str(uuid.uuid4())
        vector = self.embedder.encode(text).tolist()
        payload = {"text": text, **(metadata or {})}
        self.client.upsert(
            collection_name=config.QDRANT_COLLECTION,
            points=[qmodels.PointStruct(id=mem_id, vector=vector, payload=payload)],
        )
        return mem_id

    def search(self, query: str, top_k: int = 5):
      vector = self.embedder.encode(query).tolist()
      response = self.client.query_points(
        collection_name=config.QDRANT_COLLECTION,
        query=vector,
        limit=top_k,
    )
      return [
         {"score": round(float(h.score), 4), "text": h.payload.get("text"),
         "metadata": {k: v for k, v in h.payload.items() if k != "text"}}
        for h in response.points
    ]


    def clear(self):
     self.client.delete_collection(config.QDRANT_COLLECTION)
     self._ensure_collection()

    # in VectorMemoryStore
    def count(self) -> int:
     info = self.client.get_collection(config.QDRANT_COLLECTION)
     return info.points_count or 0