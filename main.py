from pathlib import Path
from Scripts.Ingestion import partitionDocument, createChunkByTitle
from Scripts.ChunkSummarization import summarizeChunks
from Scripts.CreateEmbeddings import createVectorStore
from utils.LoadVectorStore import loadVectorStore
from Scripts.Retriever import retrieveChunks
from Scripts.GenerateResult import generateFinalAnswer
from utils.SaveSummarizedChunks import saveSummarizedChunks, loadSummarizedChunks
from utils.AnswerSimplifier import AnswerSimplifierModels
from postprocess.CleanOutput import cleanAnswer


def main(query: str, FORCE_REBUILD=False):

    DB_PATH = "./db/chroma_db"

    if Path(DB_PATH).exists() and not FORCE_REBUILD:

        print("Loading existing vector database...")

        vector_store = loadVectorStore(DB_PATH)

    else:

        print("Building vector database from scratch...")

        documents = partitionDocument(folder_path="./dataset_2")

        elements = set([str(type(ele)) for ele in documents.keys()])
        print(f"Document partition has been created:\n{elements}")

        chunks = createChunkByTitle(documents=documents)
        print(f"\n\nChunks are created: {chunks.keys()}")

        print("Starting summarize chunks")
        summarized_chunks = summarizeChunks(chunks)
        saveSummarizedChunks(summarized_chunks)

        vector_store = createVectorStore(summarized_chunks, persist_directory=DB_PATH)

    retrieved_summarized_chunks = loadSummarizedChunks()

    retrieved_chunks = retrieveChunks(query, vector_store, retrieved_summarized_chunks)

    generated_answer = generateFinalAnswer(retrieved_chunks, query)

    answerSimplifier = AnswerSimplifierModels()
    final_answer = answerSimplifier.gemmaAnswerSimplifier(generated_answer)

    final_answer = cleanAnswer(final_answer)

    return final_answer
