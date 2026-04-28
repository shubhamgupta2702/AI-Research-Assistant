from tavily import TavilyClient
from src.graph.state import ResearchAssistantState
from src.logger.logger import logger
from dotenv import load_dotenv
import os

load_dotenv()



def search_tool(state: ResearchAssistantState) -> dict:
    """
    Tavily web-search node.
    Reads `question` from state, searches the web, and returns
    `context` (list of formatted snippets) and `sources` (list of URLs).
    """
    query = state.get("question", "")

    if not query:
        logger.warning("[SearchTool] No question in state — skipping search")
        return {"context": [], "sources": []}

    tavily_api_key = os.environ.get("TAVILY_API_KEY", "")
    if not tavily_api_key:
        logger.error("[SearchTool] TAVILY_API_KEY not set")
        return {"context": ["Tavily API key not configured."], "sources": []}

    try:
        logger.info(f"[SearchTool] Searching for: {query}")
        client   = TavilyClient(api_key=tavily_api_key)
        response = client.search(query=query, max_results=4)

    except Exception as e:
        logger.error(f"[SearchTool] Tavily search failed: {str(e)}")
        return {"context": [f"Web search failed: {str(e)}"], "sources": []}

    sources = []
    context = []

    for result in response.get("results", []):
        url     = result.get("url", "")
        title   = result.get("title", "")
        content = result.get("content", "")

        if url:
            sources.append(url)

        snippet = f"**{title}**\n{content}\nSource: {url}"
        context.append(snippet)

    logger.info(f"[SearchTool] Got {len(context)} results")
    return {"context": context, "sources": sources}

    
  
  

  