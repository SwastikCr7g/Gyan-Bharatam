import re


def parse_query(query):
    """
    Checks if the user is asking for a specific verse using regex.
    Patterns: '2.47', 'Chapter 2 Verse 47', '2:47'
    """
    # Pattern to find numbers like 2.47 or 2:47
    pattern = r'(\d+)[:.](\d+)'
    match = re.search(pattern, query)

    if match:
        return {
            "type": "direct",
            "chapter": int(match.group(1)),
            "verse": int(match.group(2))
        }

    # Check for "Chapter X Verse Y" text
    text_pattern = r'chapter\s+(\d+)\s+verse\s+(\d+)'
    match = re.search(text_pattern, query.lower())
    if match:
        return {
            "type": "direct",
            "chapter": int(match.group(1)),
            "verse": int(match.group(2))
        }

    return {"type": "conceptual", "query": query}