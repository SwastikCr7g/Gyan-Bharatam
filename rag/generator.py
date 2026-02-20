from google import genai
from config import Config
import re

def clean_shloka_text(text):
    """
    Surgically removes artifacts like --, !, (परन्तु), and pipes.
    Ensures clean Devanagari and English output.
    """
    # Remove pipes and double pipes
    text = text.replace('|', '').replace('||', '')
    # Remove artifacts: --, !, and content inside brackets like (परन्तु)
    text = re.sub(r'--|!|\(परन्तु\)', '', text)
    # Remove leading/trailing pipes and commas
    text = re.sub(r'^[|,\s]+|[|,\s]+$', '', text)
    # Remove orphaned commas often found in word-meanings
    text = re.sub(r'\s,\s', ' ', text)
    return " ".join(text.split())

def generate_answer(query, context_docs):
    client = genai.Client(api_key=Config.GOOGLE_API_KEY)

    if not context_docs:
        return "The requested information is not found in the Bhagavad Gita dataset."

    enriched_context = ""
    for doc in context_docs:
        meta = doc.get('metadata', {})
        # Clean the content at the source
        clean_content = clean_shloka_text(doc['content'])
        enriched_context += f"SOURCE: CHAPTER {meta.get('chapter')}, VERSE {meta.get('verse')}\n{clean_content}\n\n"

    prompt = f"""
    You are an expert on the Bhagavad Gita. Use the cleaned context below:
    {enriched_context}

    User Query: {query}

    Instructions:
    1. Structure each shloka section exactly like this:
       [Source: BG Chapter X, Verse Y]
       Sanskrit: (Divine Shloka)
       Hindi: (Translation)
       English: (Translation)
    2. Do NOT use any symbols like '!', '--', or brackets in the Hindi or English sections.
    3. Ensure the Sanskrit shloka is on its own separate line.
    4. Maintain a respectful, scholarly tone.
    """

    try:
        response = client.models.generate_content(
            model=Config.LLM_MODEL,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"System Error: {str(e)}"