from src.graph_store import GraphMemoryStore
from src.router import Router

gs = GraphMemoryStore()  # reuse the DB from Step 5's ingestion
router = Router(gs)

queries = [
    "What's James's job?",
    "Tell me about times I felt stressed",
    "Where does Maria live?",
    "What outdoor activities have I done?",
]

for q in queries:
    result = router.classify(q)
    print(f"{q!r}\n  -> path={result['path']}  ({result['reason']})\n")