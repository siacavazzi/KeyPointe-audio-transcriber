from lib.SQL import CONN, CURSOR
from datetime import datetime


class Overview:
    
    def __init__(self, id=None):
        self.title = ""
        self.summary = ""
        self.id = id
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        
    @classmethod
    def fetch_conversation(cls, convo_id):
        query = "SELECT * FROM conversations WHERE convo_id = ?"
        rows = CURSOR.execute(query, [convo_id]).fetchall()
        return rows
    
    @classmethod
    def get_readable_conversation(cls ,id):
        convo = cls.fetch_conversation(id)
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

    @classmethod
    def fetch_overviews(cls, limit=25):
        query = f"SELECT * FROM convo_overview LIMIT {limit}"

        rows = CURSOR.execute(query).fetchall()

        return rows




        


