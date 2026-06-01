from Scripts.Ingestion import partitionDocument, createChunkByTitle
from Scripts.ChunkSummarization import summarizeChunks

documents = partitionDocument(folder_path='./dataset_2')
elements = set([str(type(ele))for ele in documents.keys()])
print(f"Document partition has been created:\n {elements}")

chunks = createChunkByTitle(documents=documents)
print(f"\n\nChunks are created: {chunks.keys()}")

print("Starting summarize chunks")
summarized_chunks = summarizeChunks(chunks)
print(f"Created summarized chunks{summarized_chunks.keys()}")