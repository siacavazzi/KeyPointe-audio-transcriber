from lib import CONN, CURSOR
from datetime import datetime
from .GPTcontainer import get_completion

class Overview:
    
    def __init__(self):
        self.title = ""
        self.summary = ""
        self.id = None
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        Overview.create_overview_table()

    @classmethod
    def create_overview_table(cls):
        query = """
        CREATE TABLE IF NOT EXISTS convo_overview (
        id INTEGER PRIMARY KEY,
        title TEXT,
        summary TEXT,
        time TIMESTAMP
        )
        """
        CURSOR.execute(query)

            
    def initialize_convo(self):

        query = """
        INSERT INTO convo_overview
        (title, summary, time) VALUES (?,?,?)
        """
        CURSOR.execute(query, [self.title, self.summary, self.time])
        CONN.commit()

        self.id = CURSOR.lastrowid
        return self.id
        
    def fetch_conversation(self):
        query = "SELECT * FROM conversation WHERE convo_id = ?"
        rows = CURSOR.execute(query, [self.id]).fetchall()
        return rows
        


        


