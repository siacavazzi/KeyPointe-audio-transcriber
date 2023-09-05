
from lib import CONN, CURSOR
from datetime import datetime


class Conversation:
    def __init__(self, conversation_id=None):
        self.conversation_id = conversation_id
  
    @classmethod
    def create_table(cls):
        query = """
        CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY,
        time TIMESTAMP,
        convo_id INTEGER,
        content TEXT
        )
        """
        CURSOR.execute(query)

    def add_row(self, content):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        query = """
        INSERT INTO conversations
        (time, convo_id, content) VALUES (?,?,?)
        """
        CURSOR.execute(query, [current_time, self.conversation_id, content])
        CONN.commit()



        
