from src.vector_store import VectorMemoryStore

vs = VectorMemoryStore()
vs.client.delete_collection("agent_memory")
vs._ensure_collection()

vs.add_memory("My brother James just started a new job at Google.", {"speaker": "user", "date": "2024-01-10"})
vs.add_memory("I went hiking in the mountains last weekend.", {"speaker": "user", "date": "2024-01-12"})
vs.add_memory("My favorite food is Italian pasta.", {"speaker": "user", "date": "2024-01-15"})

results = vs.search("Tell me about outdoor activities I've done")
for r in results:
    print(r["score"], "-", r["text"])