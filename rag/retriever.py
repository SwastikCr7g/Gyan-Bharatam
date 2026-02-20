from rag.vector_store import get_vector_store


def retrieve_docs(parsed_query):
    vectorstore = get_vector_store()

    if parsed_query["type"] == "direct":
        chapter = parsed_query["chapter"]
        verse = parsed_query["verse"]

        # Exact metadata match for Chapter.Verse
        results = vectorstore.get(
            where={
                "$and": [
                    {"chapter": chapter},
                    {"verse": verse}
                ]
            }
        )

        if results['documents']:
            return [{"content": results['documents'][0], "metadata": results['metadatas'][0]}]
        return []

    else:
        # INCREASE K: Pull 5 verses to give the AI more context
        # We also include 'dharma' specifically in the search string
        search_query = parsed_query["query"]
        raw_results = vectorstore.similarity_search(search_query, k=5)

        formatted_results = []
        for doc in raw_results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        return formatted_results