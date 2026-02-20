from flask import Flask, render_template, request, jsonify
from rag.query_parser import parse_query
from rag.retriever import retrieve_docs
from rag.generator import generate_answer
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"})

    # 1. Parse query (Direct vs Conceptual)
    parsed = parse_query(user_query)

    # 2. Retrieve relevant verses
    docs = retrieve_docs(parsed)

    # 3. Generate Answer
    answer = generate_answer(user_query, docs)

    return jsonify({
        "answer": answer,
        "type": parsed["type"]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)