"""
Example: Web Researcher Agent — 30 lines.
Demonstrates tool-use with Unchained.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unchained import Agent, tool, LLM
import requests


@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo Instant Answer API."""
    resp = requests.get("https://api.duckduckgo.com/",
                        params={"q": query, "format": "json", "no_html": "1"},
                        timeout=10)
    data = resp.json()
    abstract = data.get("AbstractText", "")
    results = [r.get("Text", "") for r in data.get("RelatedTopics", [])[:3]
               if isinstance(r, dict)]
    return abstract or "\n".join(results) or "No results found."


agent = Agent(
    name="researcher",
    system_prompt="You are a web researcher. Use search to find accurate information. Cite your sources.",
    llm=LLM(provider="ollama", model="llama3.2"),  # Free, local
    tools=[web_search],
    verbose=True,
)

if __name__ == "__main__":
    query = input("Research query: ") if len(sys.argv) < 2 else " ".join(sys.argv[1:])
    print(agent.run(query))
