from typing import Annotated, List, Sequence
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ResearchAssistantState(BaseModel):
    """
    Represents the state of the AI Research Assistant graph.
    """
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)
    
    research_query: str = Field(
        default="", 
        description="The core question or topic the user wants researched."
    )
    
    rag_documents: List[str] = Field(
        default_factory=list, 
        description="Internal context retrieved via the RAG tool (src.tools.rag_tool)."
    )
    
    web_search_results: List[str] = Field(
        default_factory=list, 
        description="External context retrieved via the Web Search tool (src.tools.search_tool)."
    )
    
    sources: List[str] = Field(
      description="The sources from where the web search results data is fetched."
      )

    generation_attempts: int = Field(
        default=0, 
        description="Tracks the number of generation loops to prevent infinite hallucination loops."
    )
    
    is_ready_for_final_answer: bool = Field(
        default=False, 
        description="Flag to indicate if the assistant has gathered enough context to generate a final response."
    )