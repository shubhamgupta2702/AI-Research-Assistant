from src.rag.vector_store import vector_store
from src.logger.logger import logger


def get_retriever():
  """Vector Store Retriever"""
  try:
    logger.info(f'Getting Vector Store Retriever sucessfully')
    vs_store = vector_store()
    return vs_store.as_retriever(search_kwargs={"k":4})
  
  except Exception as e:
    logger.error(f'Failed to get vector store retriever:{str(e)}')
    raise e