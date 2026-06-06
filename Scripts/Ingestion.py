"""
This file loads documents and creates Chunks out of it
"""

from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
import os
from typing import List
from pathlib import Path


def partitionDocument(folder_path: str) -> dict[str, List[str]]:
    """
    Partitions the document into different elements
    """
    documents = {}
    folder = Path(folder_path)
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The directory {folder_path} does not exists")

    for pdf_file in folder.rglob("*pdf"):
        print(f"Partitioning file: {pdf_file}")

        elements = partition_pdf(
            filename=str(pdf_file),
            strategy="hi_res",  # Use the most accurate processing method for extraction (but slow)
            infer_table_structure=True,  # keep tables as structured html not jumbled text
            extract_image_block_types=["Image"],  # grab images found in the pdf
            extract_image_block_to_payload=True,  # store images as base64 you can actually use
        )

        documents[pdf_file] = elements

    if len(documents) == 0:
        raise FileNotFoundError(
            f"The .pdf file does no exists in the directory {folder_path}"
        )

    return documents


def createChunkByTitle(documents: dict) -> dict[str, List[str]]:
    """
    This Function smartly handles multiple documents dict and creates chunks for every document preserving the metadata
    """

    all_chunks = {}
    for file, elements in documents.items():
        print("Creating Smart Chunks")
        chunks = chunk_by_title(
            elements,
            max_characters=3000,
            new_after_n_chars=2400,
            combine_text_under_n_chars=600,
        )
        all_chunks[file] = chunks

    print(f"Created {len(chunks)} chunks")

    return all_chunks
