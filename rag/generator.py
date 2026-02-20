from google import genai
from config import Config
import re


def generate_answer(query, context_docs):
    """
    Generates a structured, grounded answer using the Gemini 2.5 Flash model.
    """
    client = genai.Client(api_key=Config.GOOGLE_API_KEY)

    if not context_docs:
        return "The requested information is not found in the Bhagavad Gita dataset."

    # ENHANCEMENT: Inject metadata into the text so the AI knows verse numbers
    enriched_context = ""
    for doc in context_docs:
        meta = doc.get('metadata', {})
        # Flatten content to ensure words don't break into single lines
        clean_content = " ".join(doc['content'].split())
        enriched_context += f"SOURCE: CHAPTER {meta.get('chapter')}, VERSE {meta.get('verse')}\n{clean_content}\n\n"

    prompt = f"""
    You are an expert on the Bhagavad Gita.
    Below are the relevant verses for the query:
    {enriched_context}

    User Query: {query}

    Instructions:
    1. Answer using the context above.
    2. ALWAYS mention the Chapter and Verse numbers for every shloka used.
    3. Use a structured, respectful tone with flowing paragraphs.
    4. Provide the Sanskrit Shloka first, followed by Hindi and English.
    """

    try:
        response = client.models.generate_content(
            model=Config.LLM_MODEL,
            contents=prompt
        )
        # Remove any unnecessary triple spaces from response
        return re.sub(r' {2,}', ' ', response.text.strip())
    except Exception as e:
        return f"System Error: {str(e)}"