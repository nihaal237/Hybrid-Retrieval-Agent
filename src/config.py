import os

GEMINI_MODEL = "gemini-2.5-flash"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QDRANT_PATH = os.path.join(BASE_DIR, "qdrant_data")   # embedded mode
QDRANT_COLLECTION = "agent_memory"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # small, fast, runs locally, 384-dim
EMBEDDING_DIM = 384

GRAPH_DB_PATH = os.path.join(BASE_DIR, "graph_memory.db")
SPACY_MODEL = "en_core_web_sm"