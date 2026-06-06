import json
from pathlib import Path
from langchain_core.documents import Document

def saveSummarizedChunks(summarized_chunks, save_path="./db/summarized_chunks.json"):
    """
    Saves summarized chunks in json file
    """
    print(f'\n\n Saving summarized chunks into: {save_path}')
    
    serializable_docs = {}

    for file_name, docs in summarized_chunks.items():

        serializable_docs[str(file_name)] = []

        for doc in docs:
            serializable_docs[str(file_name)].append(
                {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata
                }
            )

    Path(save_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(
            serializable_docs,
            f,
            indent=2,
            ensure_ascii=False
        )

    return f"Saved summarized chunks to {save_path}"



def loadSummarizedChunks(save_path="./db/summarized_chunks.json"):
    """
    Loads Summarized chunks from json
    """
    
    with open(save_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    summarized_chunks = {}

    for file_name, docs in data.items():

        summarized_chunks[file_name] = []

        for doc in docs:
            summarized_chunks[file_name].append(
                Document(
                    page_content=doc["page_content"],
                    metadata=doc["metadata"]
                )
            )

    return summarized_chunks
