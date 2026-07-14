import re
from .graph_store import GraphMemoryStore

# Cue words that suggest the user wants an explicit, relational fact
GRAPH_CUE_WORDS = [
    "who", "when did", "what job", "works at", "works for",
    "brother", "sister", "mother", "father", "husband", "wife",
    "son", "daughter", "friend", "married", "lives in", "job",
    "company", "relationship",
]


class Router:
    def __init__(self, graph_store: GraphMemoryStore):
        self.graph_store = graph_store

    def classify(self, query: str) -> dict:
        """
        Returns {"path": "vector"|"graph"|"hybrid", "reason": "...", "matched_entities": [...]}
        """
        query_lower = query.lower()

        # Signal 1: does the query contain relational cue words?
        cue_hit = next((cue for cue in GRAPH_CUE_WORDS if cue in query_lower), None)

        # Signal 2: does the query mention a known entity name from the graph?
        matched_entities = [
            name for name in self.graph_store.all_entity_names()
            if name.lower() in query_lower
        ]

        if cue_hit and matched_entities:
            return {"path": "graph", "reason": f"cue word '{cue_hit}' + known entity {matched_entities}",
                    "matched_entities": matched_entities}
        if matched_entities:
            return {"path": "hybrid", "reason": f"mentions known entity {matched_entities}, checking both",
                    "matched_entities": matched_entities}
        if cue_hit:
            return {"path": "graph", "reason": f"cue word '{cue_hit}' suggests a relational fact",
                    "matched_entities": []}
        return {"path": "vector", "reason": "no relational cues or known entities detected",
                "matched_entities": []}