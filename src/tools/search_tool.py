from tavily import TavilyClient
from graph.state import ResearchAssistantState
from src.logger.logger import logger
import os

TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]

def search_tool(state: ResearchAssistantState):
  query = state.get("question")
  
  if not query:
    return {}
  
  try:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(query=query,max_results=4)
    
  except Exception as e:
    state.web_search_results.extend(f"Search Failed: {str(e)}")
    logger.error("Tavily Web Search Failed")
    return {
            "context": [f"Search Failed: {str(e)}"]
        }
    
  sources =  []
  context = []
  for r in response.get("results",[]):
    url = r.get("url","")
    sources.append(url)
    
    content = f"{r.get('title', '')}\n{r.get('content', '')}\n{r.get('url', '')}"
    content.append(content)

  return {
    "context": context,
    "sources": sources
  }
    
  
  

  