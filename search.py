import os
from tavily import TavilyClient


def get_tavily_client():
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str) -> str:
    """
    Performs deep Tavily search and returns structured context string.
    Designed to reduce hallucination via:
    - max_results=7
    - search_depth='advanced'
    - include_raw_content=True
    - Filters out thin/TOC pages (< 200 chars)
    - Increased content limit to 3000 chars per source
    """

    client = get_tavily_client()

    print(f"\n🔍 Searching Tavily for: '{query}'...\n")

    try:
        response = client.search(
            query,
            max_results=7,
            search_depth="advanced",
            include_raw_content=True,
        )

        combined_text = ""
        skipped = 0

        for i, result in enumerate(response.get("results", []), 1):

            content = result.get("raw_content") or result.get("content", "")

            # Skip thin/TOC pages
            if len(content.strip()) < 200:
                skipped += 1
                continue

            combined_text += f"[SOURCE {i}] {result.get('title', 'No Title')}\n"
            combined_text += f"URL: {result.get('url', 'N/A')}\n"
            combined_text += f"CONTENT:\n{content[:3000]}\n\n"
            combined_text += f"{'─' * 60}\n\n"

        if skipped > 0:
            print(f"⚠ Skipped {skipped} thin/TOC sources.\n")

        if not combined_text.strip():
            return "No search results found."

        return combined_text

    except Exception as e:
        print(f"⚠ Search error: {e}")
        return "No search results found due to an error."