from flask import Flask, render_template, request, jsonify, send_file
from rag.query_parser import parse_query
from rag.retriever import retrieve_docs
from rag.generator import generate_answer
import edge_tts
import asyncio
import os

app = Flask(__name__)

# Ensure a folder exists for temporary audio files
AUDIO_DIR = "static/audio"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"})

    # 1. Parse query
    parsed = parse_query(user_query)

    # 2. Retrieve relevant verses
    docs = retrieve_docs(parsed)

    # 3. Generate Answer (Now using the cleaned generator)
    answer = generate_answer(user_query, docs)

    return jsonify({
        "answer": answer,
        "type": parsed["type"]
    })


@app.route('/read', methods=['POST'])
def read_shloka():
    """
    Converts Sanskrit/Hindi text to a human-like audio file.
    """
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"})

    # Clean the text for TTS (remove brackets/metadata)
    clean_text = text.split(']')[-1].strip()

    output_path = os.path.join(AUDIO_DIR, "recitation.mp3")

    # Use a high-quality Indian English or Hindi voice for Sanskrit
    # 'hi-IN-MadhurNeural' is excellent for spiritual text
    voice = "hi-IN-MadhurNeural"

    async def generate_audio():
        communicate = edge_tts.Communicate(clean_text, voice)
        await communicate.save(output_path)

    try:
        asyncio.run(generate_audio())
        return send_file(output_path, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)