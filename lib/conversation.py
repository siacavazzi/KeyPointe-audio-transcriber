
from lib import CONN, CURSOR
from datetime import datetime
from .overview import Overview


class Conversation:
    def __init__(self):
        overview = Overview()

        self.conversation_id = overview.initialize_convo()

    # create reference in overview table with id

    
    @classmethod
    def get_highest_id(cls):
        CURSOR.execute("SELECT MAX(convo_id) FROM conversations")
        highest_id = CURSOR.fetchone()[0]
        return highest_id if highest_id else 0

  
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

    @classmethod
    def reset_table(cls):
        query = "DROP TABLE conversations"
        CURSOR.execute(query)
        CONN.commit()
        cls.create_table()





        
