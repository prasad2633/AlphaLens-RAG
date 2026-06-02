from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

def createVectorStore(documents:str, persist_directory='./db/chroma_db'):
    """
    This creates vector store using the chunks
    """
    print("Creating embedding and storing it in Chroma DB")
    flat_doc = []

    for file_name, docs in documents.items():
        print(f'Flattening for file name {file_name}')
        flat_doc.extend(docs)
    
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = Chroma.from_documents(
        documents=flat_doc,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space": "cosine"}
        )

    print("Created vector store")
    return vector_store

