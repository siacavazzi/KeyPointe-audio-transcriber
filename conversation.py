
class Conversation:
    def __init__(self):
        pass

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY,
        time TIMESTAMP,
        convo_id INTEGER,
        content TEXT,
        )
        """
        