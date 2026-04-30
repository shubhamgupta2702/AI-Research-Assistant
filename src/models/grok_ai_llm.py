from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

@traceable(run_type="llm")
def get_grokai_llm():
    """Plain Grok AI LLM — use this for generation / routing."""
    return ChatGroq(model="groq/compound-mini")
