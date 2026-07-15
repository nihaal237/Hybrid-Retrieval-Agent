import json
from .vector_store import VectorMemoryStore
from .graph_store import GraphMemoryStore
from .extractor import extract_relations


def ingest_conversation(path: str, vector_store: VectorMemoryStore, graph_store: GraphMemoryStore):
    with open(path, "r") as f:
        data = json.load(f)

    turn_count = 0
    relation_count = 0

    for session in data["sessions"]:
        session_id = session["session_id"]
        date = session["date"]

        for i, turn in enumerate(session["turns"]):
            turn_id = f"{session_id}_turn{i}"
            speaker = turn["speaker"]
            text = turn["text"]

            # 1. Vector store: every turn, regardless of content
            vector_store.add_memory(text, metadata={
                "speaker": speaker, "date": date, "turn_id": turn_id,
            })
            turn_count += 1

            # 2. Graph store: only turns that yield extractable facts
            relations = extract_relations(text, speaker=speaker) #if relations extracted then save in graph

            for rel in relations:
                graph_store.add_relation(
                    rel["subject"], rel["predicate"], rel["object"],
                    subject_type=rel["subject_type"], object_type=rel["object_type"],
                    raw_text=text, timestamp=date,
                )
                relation_count += 1

    return {"turns_ingested": turn_count, "relations_extracted": relation_count}