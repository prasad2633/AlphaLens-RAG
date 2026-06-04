from langchain_classic.retrievers import EnsembleRetriever, BM25Retriever
from langchain_cohere import CohereRerank
from dotenv import load_dotenv

load_dotenv()

def retrieveChunks(query:str, db, documents):
    """
    This uses both vector retriever (semantic search/ dense retriever) and BM25 retriever (Keyword Search/ Sparse Retrieval) 
    And Reranks the retrieved docs  
    """
    
    vector_retriever=db.as_retriever(search_kwargs={"k":10})
    
    all_docs = []
    
    for file_name, doc in documents.items():
        all_docs.extend(doc)
        
    bm25_retriever = BM25Retriever.from_documents(all_docs)
    bm25_retriever.k = 10

    hybrid_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.7, 0.3]
    )
    
    retrieved_chunks=hybrid_retriever.invoke(query)

    reranker = CohereRerank(model="rerank-english-v3.0", top_n=5)
    reranked_doc = reranker.compress_documents(retrieved_chunks, query)

    return reranked_doc