from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import os

ASTRA_DB_API_ENDPOINT = os.environ["ASTRA_DB_API_ENDPOINT"]
ASTRA_DB_APPLICATION_TOKEN = os.environ["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_KEYSPACE = os.environ["ASTRA_DB_KEYSPACE"]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def vector_store():
  
  vector_store = AstraDBVectorStore(
            embedding=embeddings,
            collection_name="ai_research_assistant",
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,
            namespace=ASTRA_DB_KEYSPACE,
        )
  return vector_store
  