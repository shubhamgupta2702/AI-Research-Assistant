from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.logger.logger import logger
from src.rag.vector_store import vector_store


async def ingest_pdf(filepath:str):
  """Load PDF from filepath using PDF Loader, then chunk it, generate embeddings and ingest it into AstraDB."""
  
  try:
    logger.info(f"PDF is processing:{filepath}")
    loader = PyPDFLoader(file_path=filepath)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    splitted_text = text_splitter.split_documents(docs)
    
    vstore = vector_store()
    vstore.add_documents(splitted_text)
    
    logger.info(f"Successfully added chunks to vector database AstraDB: chunk_size={len(splitted_text)}, file_path:{filepath}")
    
  except Exception as e:
    logger.error(f"Document ingestion failed of filepath:{filepath} into DB with error:{str(e)}")
    raise e
  
