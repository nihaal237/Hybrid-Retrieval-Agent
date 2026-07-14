from google import genai
from . import config

client = genai.Client()  # reads GEMINI_API_KEY from env automatically


def format_evidence(vector_results, graph_results) -> str:
    lines = []
    for g in graph_results:
        lines.append(f"- {g['subject']} {g['predicate'].replace('_', ' ')} {g['object']} (from {g['timestamp']})")
    for v in vector_results:
        lines.append(f"- \"{v['text']}\" (relevance score {v['score']})")
    return "\n".join(lines) if lines else "No relevant memories found."


def synthesize_answer(query: str, vector_results, graph_results) -> str:
    evidence = format_evidence(vector_results, graph_results)

    if not vector_results and not graph_results:
        return "I don't have any memory of that."

    prompt = f"""You are answering a question using only the facts retrieved from a memory system below. Be concise -- one or two sentences. If the facts don't actually answer the question, say so honestly.

Question: {query}

Retrieved facts:
{evidence}

Answer:"""

    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt,
    )
    return response.text