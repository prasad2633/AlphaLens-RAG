from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

def loadVectorStore(persist_directory="./db/chroma_db"):

    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )

    return vector_store