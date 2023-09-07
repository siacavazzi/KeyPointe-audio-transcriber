import sqlite3

CONN = sqlite3.connect('db/convo_database.db', check_same_thread=False)
CURSOR = CONN.cursor()
