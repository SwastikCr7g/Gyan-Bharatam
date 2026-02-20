from datasets import load_dataset
from langchain_core.documents import Document


def load_gita_dataset():
    print("Fetching Bhagavad Gita dataset from HuggingFace...")
    # Loading the specific dataset from your screenshot
    ds = load_dataset("JDhruv14/Bhagavad-Gita_Dataset")
    data = ds['train']

    documents = []

    for row in data:
        # Using exact lowercase keys from your dataset viewer
        sanskrit = row['sanskrit']
        hindi = row['hindi']
        english = row['english']

        # Combine for embedding search
        content = f"Sanskrit: {sanskrit}\nHindi: {hindi}\nEnglish: {english}"

        # Metadata for direct Chapter.Verse lookup
        metadata = {
            "chapter": int(row['chapter']),
            "verse": int(row['verse']),
            "transliteration": row['transliteration']
        }

        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    print(f"✅ Successfully loaded {len(documents)} verses.")
    return documents


if __name__ == "__main__":
    verses = load_gita_dataset()
    if verses:
        print(f"Sample Verse 1.1 Content:\n{verses[0].page_content}")