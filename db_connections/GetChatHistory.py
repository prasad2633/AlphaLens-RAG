from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
import sqlite3

def get_chat_history(conversation_id, conn, c):
    
    c.execute(
        """
        SELECT user_question, assistant_answer
        FROM chat_turns
        WHERE conversation_id = ?
        ORDER BY id
        """,
        (conversation_id,)
    )

    rows = c.fetchall()

    history = []

    for user_question, assistant_answer in rows:
        
        history.append(
            HumanMessage(content=user_question)
        )

        history.append(
            AIMessage(content=assistant_answer)
        )

    return history