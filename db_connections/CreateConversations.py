
def create_conversation(conversation_id, conn, c):

    c.execute(
        """
        INSERT OR IGNORE INTO conversations (
            conversation_id
        )
        VALUES (?)
        """,
        (conversation_id,)
    )

    conn.commit()