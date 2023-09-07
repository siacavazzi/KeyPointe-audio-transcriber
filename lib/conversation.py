
from lib.SQL import CONN, CURSOR
from datetime import datetime
from lib.overview import Overview
from lib.GPTcontainer import get_completion
import ast


class Conversation:
    def __init__(self):
        self.overview = Overview()
        self.conversation_id = self.overview.initialize_convo()
        Conversation.create_table()

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
        current_time = datetime.now().strftime('%H:%M:%S')
        query = """
        INSERT INTO conversations
        (time, convo_id, content) VALUES (?,?,?)
        """
        CURSOR.execute(query, [current_time, self.conversation_id, content])
        CONN.commit()

    @classmethod
    def reset_table(cls, table):
        query = f"DROP TABLE {table}"
        CURSOR.execute(query)
        CONN.commit()

    def end_conversation(self):
        print("ending convo")
        convo = Overview.get_readable_conversation(self.overview.id)

        print(f"conversation: {convo}")

        prompt = """
        Provide a title and summary for the following transcript formatted as a Python dictionary with no other text. 
        Keep in mind that the transcript may be imperfect.
        Your output should look like this with your text:
        {
        'title': 'Placeholder Title',
        'summary': 'This is a placeholder summary.'
        } \n
        """ + convo

        response = get_completion(prompt)


        try:
            titleSummary = ast.literal_eval(response)
        except:
            titleSummary = None
        
        self.overview.add_title_summary(titleSummary)


    @classmethod
    def reset_database(cls):
        cls.reset_table("conversations")
        cls.reset_table("convo_overview")

    @classmethod
    def delete_convo(cls, id):
        query1 = "DELETE FROM conversations WHERE convo_id = ?"
        query2 = "DELETE FROM convo_overview WHERE id = ?"
        CURSOR.execute(query1, [id])
        CURSOR.execute(query2, [id])
        CONN.commit()

    @classmethod
    def export(cls, id):
        pass









        
