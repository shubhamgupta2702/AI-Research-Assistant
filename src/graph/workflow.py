from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from src.graph.state import ResearchAssistantState
from src.rag.retriever import get_retriever
from src.tools.search_tool import search_tool
from src.logger.logger import logger
from langsmith import traceable
import os

@traceable(run_type="llm")
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0)

@traceable
def route_question(state: ResearchAssistantState) -> ResearchAssistantState:
    question = state.get("question", "")
    logger.info(f"[Router] Analyzing: {question}")

    router_prompt = PromptTemplate.from_template(
        """Analyze the user question. Determine if it needs:
        1. 'rag': Only internal documents (e.g., specific company data, PDFs).
        2. 'web_search': Only general/current web info.
        3. 'both': Needs internal context AND web updates for a refined answer.

        Respond with ONLY one word: 'rag', 'web_search', or 'both'.
        Question: {question}"""
    )

    chain = router_prompt | get_llm() | StrOutputParser()
    route = chain.invoke({"question": question}).strip().lower()
    
    if route not in ["rag", "web_search", "both"]:
        route = "both"
    
    return {"route": route}

@traceable
def retrieve(state: ResearchAssistantState) -> ResearchAssistantState:
    question = state.get("question", "")
    logger.info("[Retriever] Fetching from Vector Store...")
    try:
        retriever = get_retriever()
        docs = retriever.invoke(question)
        context = [doc.page_content for doc in docs]
        sources = [doc.metadata.get("source", "Knowledge Base") for doc in docs]
        return {"context": context, "sources": sources}
    except Exception as e:
        logger.error(f"RAG Error: {e}")
        return {"context": ["RAG retrieval failed."]}


@traceable
def generate(state: ResearchAssistantState) -> ResearchAssistantState:
    """The LLM takes everything found so far and creates a refined response."""
    question = state.get("question", "")
    context  = state.get("context", [])
    
    
    logger.info("[Generator] Refining final response with LLM synthesis...")

    generate_prompt = PromptTemplate.from_template(
        """You are an advanced Research Assistant. 
        Your task is to synthesize the provided context into a professional, refined answer.
        
        Rules:
        1. If RAG data and Web data conflict, prioritize RAG for internal facts.
        2. Use a professional tone.
        3. Mention if the information came from internal docs or the web.

        Context:
        {context}

        Question: {question}

        Refined Answer:"""
    )

    context_str = "\n\n---\n\n".join(context) if context else "No context available."
    chain = generate_prompt | get_llm() | StrOutputParser()
    generation = chain.invoke({"context": context_str, "question": question})

    return {"generation": generation}


@traceable
def build_workflow():
    workflow = StateGraph(ResearchAssistantState)

    workflow.add_node("router", route_question)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("web_search", search_tool)
    workflow.add_node("generate", generate)

    workflow.set_entry_point("router")

    # Conditional edge
    workflow.add_conditional_edges(
        "router",
        lambda x: x["route"],
        {
            "rag": "retrieve",
            "web_search": "web_search",
            "both": "retrieve"
        }
    )

    workflow.add_edge("retrieve", "web_search")
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()

workflow = build_workflow()