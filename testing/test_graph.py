from src.graph_store import GraphMemoryStore

gs = GraphMemoryStore("test_graph.db")
gs.add_relation("James", "works_at", "Google", "person", "org",
                 raw_text="My brother James just started a new job at Google.",
                 timestamp="2024-01-10")
gs.add_relation("James", "is_brother_of", "Me", "person", "person",
                 raw_text="My brother James...", timestamp="2024-01-10")

results = gs.get_relations_for_entity("James")
for r in results:
    print(f"{r['subject']} --[{r['predicate']}]--> {r['object']}  ({r['timestamp']})")