from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from Scripts.Retriever import retrieveChunks
from Scripts.GenerateResult import generateFinalAnswer
import sqlite3
from db_connections.GetChatHistory import get_chat_history
from db_connections.CreateConversations import create_conversation

conn = sqlite3.connect('./db/sqlDB', check_same_thread=False)
c = conn.cursor()

def historyAwareGeneration(user_question, db, documents, conversation_id):
    
    create_conversation(conversation_id, conn, c)
    chat_history = get_chat_history(conversation_id, conn, c)
    if chat_history:
        messages = [SystemMessage(content="Given the chat history, rewrite the new question to be standalone and searchable. Just rewritten question.")] + chat_history + [
            HumanMessage(content=f"New Question: {user_question}")
            ]
        model = ChatOllama(model='gemma3:latest')
        result = model.invoke(messages)
        search_question = result.content.strip()
        print(f"Searching for: {search_question}")
        
    else:
        search_question = user_question
        print(f"Searching for: {search_question}")

    relevant_docs = retrieveChunks(search_question, db, documents)
    
    result = generateFinalAnswer(relevant_docs, search_question)
    
    c.execute(
        """
        INSERT INTO chat_turns (
            conversation_id,
            user_question,
            rewritten_query,
            assistant_answer
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            conversation_id,
            user_question,
            search_question,
            result
        )
    )   
    
    print(f"Answer: {result}")
    
    return result