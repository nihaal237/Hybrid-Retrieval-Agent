from src.memory_system import MemorySystem

ms = MemorySystem()
print("Stats:", ms.stats())

for q in ["What's James's job?", "Tell me about times I felt stressed"]:
    result = ms.query(q)
    print(f"\nQuery: {q}")
    print("  Routing:", result["routing"]["path"], "-", result["routing"]["reason"])
    print("  Vector hits:", len(result["vector_results"]))
    print("  Graph hits:", len(result["graph_results"]))
    for g in result["graph_results"]:
        print("   ", g["subject"], "-[", g["predicate"], "]->", g["object"])