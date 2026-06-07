import sqlite3

def createTables():

    conn = sqlite3.connect('./db/sqlDB')
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS conversations (
        conversation_id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")

    c.execute("""CREATE TABLE IF NOT EXISTS chat_turns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT,
        user_question TEXT,
        rewritten_query TEXT,
        assistant_answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")

    conn.commit()

    conn.close()