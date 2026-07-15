# Hybrid Retrieval Agent

Vector search + knowledge graph retrieval, routed per query, with LLM-synthesized answers.

A personal-assistant-style memory system that combines **vector search** (Qdrant) with a **knowledge graph** (SQLite) instead of relying on vector search alone. A router decides, per query, whether the question needs semantic recall ("what feels similar to this?"), explicit graph facts ("what's my brother's job?"), or both — then Gemini synthesizes a grounded natural-language answer from whatever evidence is retrieved.

Inspired by the **LoCoMo** long-conversation memory benchmark and the limitations of pure vector-based memory: vector search is good at fuzzy semantic similarity but unreliable at precise relational facts stated once, weeks ago. This project pairs both retrieval styles and shows, per answer, which path actually resolved the query.

## Why hybrid?

| Query | Best retrieval | Why |
|---|---|---|
| "Tell me about times I felt stressed" | Vector | Vague, semantic, no single fact |
| "What's James's job?" | Graph | A specific, explicitly-stated fact |
| "Where does Maria live?" | Hybrid | Named entity, benefits from both |

Pure vector search treats both cases the same way and often surfaces something merely *related* rather than the actual fact. The graph store holds facts as explicit `(subject, predicate, object)` triples, so precise questions get precise answers.

**Ingestion (write path):** every conversation turn is embedded and stored in the vector store unconditionally; only turns matching an extraction pattern (family, job, location facts) add an edge to the graph. Most conversation is small talk — the graph stays curated, not a dumping ground.

**Query (read path):** the router inspects the question for relational cue words and known entity names, picks `vector`, `graph`, or `hybrid`, `memory_system.py` fetches evidence accordingly, and `synthesizer.py` turns that evidence into a one-or-two-sentence answer — explicitly instructed to say so if the evidence doesn't actually answer the question, rather than inventing details.

## Stack

- **Vector recall:** Qdrant (embedded/local mode — no server required)
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`, runs locally)
- **Graph store:** SQLite (entities + relations tables; swappable for Neo4j)
- **Entity/relation extraction:** spaCy NER + targeted regex patterns
- **Answer synthesis:** Google Gemini API
- **Backend:** Flask
- **Frontend:** vanilla HTML/JS

## Architecture

```mermaid
flowchart TD
    A[User Query]

    A --> B[Router<br/>Classifies query using cue words + known entity matching]

    B --> C[Vector Store<br/>Qdrant (Embedded)<br/>Semantic similarity search]
    B --> D[Graph Store<br/>SQLite<br/>Entity relationship lookup]

    C --> E[Gemini<br/>Synthesizes a grounded answer]
    D --> E

    E --> F[Flask API + Web UI<br/>Displays answer, routing decision, and retrieved evidence]
```

## Skills demonstrated

Retrieval-Augmented Generation (RAG) · Vector search & embeddings · Knowledge graph design · LLM integration & prompt engineering · Natural Language Processing (NER, entity/relation extraction) · Python · Flask / REST API design · System architecture & pipeline design

## Usage

1. Click **"Ingest sample conversation"** to populate both stores from `data/sample_locomo.json`.
2. Ask a question — try the suggested chips, or your own:
   - *"What's James's job?"* → routes to **graph**
   - *"Tell me about times I felt stressed"* → routes to **vector**
   - *"Where does Maria live?"* → routes to **hybrid**
3. Each answer shows a routing badge, the reasoning behind that routing decision, and the raw evidence (scored vector snippets and/or graph triples) that produced it.
4. Use **"Reset all memory"** to clear both stores before re-ingesting (ingestion doesn't dedup, so re-ingesting without resetting will duplicate memories).

## Known limitations

- Relation extraction uses regex patterns tuned for family/job/location facts stated in a fairly direct sentence structure; more complex phrasing can be missed. A production system would typically use an LLM call for extraction instead.
- The router uses keyword/entity-matching heuristics rather than a learned classifier.
- SQLite graph store is a simplified stand-in for a real graph database (Neo4j) — same interface, so it's a drop-in swap.
- No deduplication on re-ingestion.

## Possible extensions

- Swap SQLite for Neo4j with Cypher queries for multi-hop graph traversal
- Add job-title / event / date-based relation extraction
- Replace regex extraction with LLM-based structured extraction
- Add content-hash deduplication on ingest
- Load the full LoCoMo benchmark dataset instead of the sample conversation
- Add multi-turn conversational memory (not just single-shot Q&A)
