import shutil, os
from src.vector_store import VectorMemoryStore
from src.graph_store import GraphMemoryStore
from src.ingest import ingest_conversation

# clean slate
if os.path.exists("qdrant_data"):
    shutil.rmtree("qdrant_data")
if os.path.exists("graph_memory.db"):
    os.remove("graph_memory.db")

vs = VectorMemoryStore()
gs = GraphMemoryStore()

stats = ingest_conversation("data/sample_locomo.json", vs, gs)
print("Ingestion stats:", stats)

print("\n--- Vector search: 'stressful things going on' ---")
for r in vs.search("stressful things going on", top_k=3):
    print(f"  {r['score']}  {r['text']}")

print("\n--- Graph query: 'James' ---")
for r in gs.get_relations_for_entity("James"):
    print(f"  {r['subject']} --[{r['predicate']}]--> {r['object']}  ({r['timestamp']})")

print("\n--- Graph query: 'Maria' ---")
for r in gs.get_relations_for_entity("Maria"):
    print(f"  {r['subject']} --[{r['predicate']}]--> {r['object']}  ({r['timestamp']})")