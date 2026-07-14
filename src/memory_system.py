from .vector_store import VectorMemoryStore
from .graph_store import GraphMemoryStore
from .router import Router
from .ingest import ingest_conversation
from .synthesizer import synthesize_answer


class MemorySystem:
    def __init__(self):
        self.vector_store = VectorMemoryStore()
        self.graph_store = GraphMemoryStore()
        self.router = Router(self.graph_store)

    def ingest(self, path: str):
        return ingest_conversation(path, self.vector_store, self.graph_store)

    def query(self, user_query: str, top_k: int = 5) -> dict:
        decision = self.router.classify(user_query)
        path = decision["path"]

        vector_results = []
        graph_results = []

        if path in ("vector", "hybrid"):
            vector_results = self.vector_store.search(user_query, top_k=top_k)

        if path in ("graph", "hybrid"):
            for entity in decision["matched_entities"]:
                graph_results.extend(self.graph_store.get_relations_for_entity(entity))
            if not decision["matched_entities"]:
                # fallback: no named entity matched, try a loose keyword search
                for word in user_query.split():
                    graph_results.extend(self.graph_store.search_by_keyword(word))

        answer = synthesize_answer(user_query, vector_results, graph_results)

        return {
            "query": user_query,
            "answer": answer,
            "routing": decision,
            "vector_results": vector_results,
            "graph_results": graph_results,
        }

    def stats(self) -> dict:
        return {
            "vector_count": self.vector_store.count(),
            "graph_counts": self.graph_store.counts(),
        }