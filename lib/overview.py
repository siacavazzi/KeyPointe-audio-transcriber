from lib import CONN, CURSOR
from datetime import datetime


class Overview:
    
    def __init__(self, id=None):
        self.title = ""
        self.summary = ""
        self.id = id
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
        
    def fetch_conversation(self, convo_id=None):
        if convo_id is None:
            convo_id = self.id
        query = "SELECT * FROM conversations WHERE convo_id = ?"
        rows = CURSOR.execute(query, [convo_id]).fetchall()
        return rows
    
    def get_readable_conversation(self, convo_id=None):
        convo = self.fetch_conversation(convo_id)
        output = ''
        for row in convo:
            timestamp = row[1]
            time = timestamp[11:19]
            output += f"{time}:{row[3]}\n" 
        return output
    
    def add_title_summary(self, data):
        query = """
        UPDATE convo_overview
        SET title = ?, summary = ?
        WHERE id = ?
        """
        try:
            CURSOR.execute(query, [data['title'], data['summary'], self.id])
        except:
            CURSOR.execute(query, ["Untitled", "Summary Missing", self.id])
        CONN.commit()




        


