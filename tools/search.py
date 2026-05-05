import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_company(query: str) -> dict:
    """
    Search for company information using Serper API.
    Returns structured search results.
    """
    if not SERPER_API_KEY:
        raise ValueError("SERPER_API_KEY not found in environment variables")

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": 5
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })

        knowledge_graph = data.get("knowledgeGraph", {})

        return {
            "query": query,
            "results": results,
            "knowledge_graph": {
                "title": knowledge_graph.get("title", ""),
                "type": knowledge_graph.get("type", ""),
                "description": knowledge_graph.get("description", ""),
                "website": knowledge_graph.get("website", "")
            }
        }

    except requests.exceptions.RequestException as e:
        return {
            "query": query,
            "results": [],
            "knowledge_graph": {},
            "error": str(e)
        }


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Anthropic AI company"
    result = search_company(query)
    print(json.dumps(result, indent=2))
