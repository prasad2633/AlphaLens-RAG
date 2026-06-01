import json
from typing import List

from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

from langchain_core.documents import Document
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage


from typing import List

def mergeTablesWithContext(chunks:str) -> List[str]:
    merged = []
    
    for i, chunk in enumerate(chunks):
        if type(chunk).__name__ == 'Table':
            if merged:
                prev = merged[-1]
                
                # add table into prev chunk's orig_elements
                if hasattr(prev, 'metadata'):
                    if hasattr(prev.metadata, 'orig_elements') and prev.metadata.orig_elements:
                        prev.metadata.orig_elements.append(chunk)  # ← append Table element
                    else:
                        prev.metadata.orig_elements = [chunk]  # ← create if doesn't exist
            else:
                merged.append(chunk)  # table at start, no prev chunk
        else:
            merged.append(chunk)
    
    return merged

def createAiEnhancedSummary(text: str, tables: List[str], images: List[str]) -> str:
    try:
        llm = ChatOllama(model="gemma3:latest")

        # Build Text Prommpt
        prompt_text = f"""
        You are creating a searchable description for document content retrieval.

        CONTENT TO ANALYZE:
        TEXT CONTENT:
        {text}
        
        """ 
        if tables or images:
            prompt_text += "Tables:\n"

            prompt_text += """
            YOUR TASK:
            Generate a comprehensive, searchable description that covers:

            1. Key facts, numbers and data points from text and tables.
            2. Main topics and concepts discussed 
            3. Questions this content could answer
            4. Visual content analysis(charts, diagrams, patterns in images)
            5. Alternative search terms users might use

            Make it crisp and searchable - prioritize findability over brevity.

            SEARCHABLE DESCRIPTION:
            """ 

        message_content = [{"type": "text", "text": prompt_text}]

        for image_base64 in images:
            message_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                })

        message = HumanMessage(content = message_content)
        response = llm.invoke([message])

        return response.content

    except Exception as e:
        print(f"AI summary failed: {e}")
        summary = f"text: {text[:300]}...."
        
        if tables:
            summary += f"Contains {len(tables)} table(s)"
        if images:
            summary += f"Contains {len(images)} image(s)"

        return summary

def seperateContentTypes(chunk:str) -> dict[str,List[str]]:
    content_data = {
        'text': chunk.text,
        'tables': [],
        'images': [],
        'types': ['text'],
        }

    # check for tables and images
    if hasattr(chunk, 'metadata') and hasattr(chunk.metadata, 'orig_elements'):
        for element in chunk.metadata.orig_elements:
            element_type = type(element).__name__

            if element_type == 'Table':
                content_data['types'].append('table')
                table_html = getattr(element.metadata, 'text_as_html', element.text)    
                content_data['tables'].append(table_html)
                
            elif element_type == 'Image':
                if hasattr(element, 'metadata') and hasattr(element.metadata, 'image_base64'):
                    content_data['types'].append('image')
                    content_data['images'].append(element.metadata.image_base64)

    content_data['types'] = list(set(content_data['types']))

    return content_data
            

def summarizeChunks(all_chunks:dict) -> dict[str, List[str]]:
    print("Processing chunks with AI summarization")
    
    all_langchain_doc = {}
    
    for file_name, chunks in all_chunks.items():
        print(f"Processing document {file_name}")
        
        merged_chunks = mergeTablesWithContext(chunks)
        langchain_doc = []
        total_chunks = len(chunks)
        
        for i, chunk in enumerate(merged_chunks):
            current_chunk = i+1
            print(f"Processing chunk: {current_chunk}/{total_chunks}")

            content_data = seperateContentTypes(chunk)

            if content_data['tables'] or content_data['images']:
                print('Creating AI summary for mixed content')
                try:
                    enhanced_content = createAiEnhancedSummary(
                        content_data['text'],
                        content_data['tables'],
                        content_data['images']
                        )
                except Exception as e:
                    print(f" AI summary failed: {e}")

            else:
                print(f" Using raw text (no tables/ images)")
                enhanced_content = content_data['text']

            doc = Document(
                page_content=enhanced_content,
                metadata={
                    "original_content": json.dumps({
                        "raw_text": content_data['text'],
                        "table_html": content_data['tables'],
                        "image_base64": content_data['images']
                        })
                    }
                )

            langchain_doc.append(doc)

            print(f"Completed Summarizing chunk {current_chunk}")
            
        all_langchain_doc[file_name] = langchain_doc

    return all_langchain_doc

