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

        if cue_hit and matched_entities: #query has both a relational keyword and a known name(entity) → go straight to graph.
            return {"path": "graph", "reason": f"cue word '{cue_hit}' + known entity {matched_entities}",
                    "matched_entities": matched_entities}
        if matched_entities: #no cue word, but a known name(entity) is mentioned → check both stores just in case.
            return {"path": "hybrid", "reason": f"mentions known entity {matched_entities}, checking both",
                    "matched_entities": matched_entities}
        if cue_hit: #a relational keyword is there, but no recognized name → still try the graph.
            return {"path": "graph", "reason": f"cue word '{cue_hit}' suggests a relational fact",
                    "matched_entities": []}
        return {"path": "vector", "reason": "no relational cues or known entities detected",  # neither signal found → default to semantic search.
                "matched_entities": []}