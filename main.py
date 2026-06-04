from Scripts.Ingestion import partitionDocument, createChunkByTitle
from Scripts.ChunkSummarization import summarizeChunks
from Scripts.CreateEmbeddings import createVectorStore
from Scripts.Retriever import retrieveChunks
from Scripts.GenerateResult import generateFinalAnswer

documents = partitionDocument(folder_path='./dataset_2')
elements = set([str(type(ele))for ele in documents.keys()])
print(f"Document partition has been created:\n {elements}")

chunks = createChunkByTitle(documents=documents)
print(f"\n\nChunks are created: {chunks.keys()}")

print("Starting summarize chunks")
summarized_chunks = summarizeChunks(chunks)

vector_store = createVectorStore(summarized_chunks)

query = 'Can you explain me about Multi head attention'
retrieved_chunks = retrieveChunks(query, vector_store, summarized_chunks)

final_answer = generateFinalAnswer(retrieveChunks, query)
print(f"Final answer: {final_answer}")