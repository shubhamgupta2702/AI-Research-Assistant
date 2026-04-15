from tavily import TavilyClient
from graph.state import ResearchAssistantState
from src.logger.logger import logger
import os

TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]

def search_tool(state: ResearchAssistantState):
  query = state.research_query
  
  if not query:
    return
  
  #check for web_search_results and sources are not none
  if not hasattr(state, "web_search_results") or state.web_search_results is None:
      state.web_search_results = []

  if not hasattr(state, "sources") or state.sources is None:
      state.sources = []
  
  try:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(query=query,max_results=4)
    
  except Exception as e:
    state.web_search_results.extend(f"Search Failed: {str(e)}")
    logger.error("Tavily Web Search Failed")
    return state.web_search_results
    
  
  for r in response.get("results",[]):
    url = r.get("url","")
    if url and url not in state.sources:
      state.sources.append(url)
    
    content = f"{r.get('title', '')}\n{r.get('content', '')}\n{r.get('url', '')}"
    state.web_search_results.append(content)
    
  
  

  