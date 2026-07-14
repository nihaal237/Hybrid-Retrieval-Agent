from flask import Flask, request, jsonify, send_from_directory
from .memory_system import MemorySystem

app = Flask(__name__, static_folder="../static", static_url_path="")
ms = MemorySystem()


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/stats")
def stats():
    return jsonify(ms.stats())


@app.route("/api/ingest", methods=["POST"])
def ingest():
    result = ms.ingest("data/sample_locomo.json")
    return jsonify(result)


@app.route("/api/query", methods=["POST"])
def query():
    body = request.get_json()
    user_query = body.get("query", "")
    if not user_query:
        return jsonify({"error": "query is required"}), 400
    result = ms.query(user_query)
    return jsonify(result)

@app.route("/api/reset", methods=["POST"])
def reset():
    ms.vector_store.clear()
    ms.graph_store.clear()
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)