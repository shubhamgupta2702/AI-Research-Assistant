from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

@traceable(run_type="llm")
def get_llm():
    """Plain Gemini LLM — use this for generation / routing."""
    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        temperature=0,
    )
