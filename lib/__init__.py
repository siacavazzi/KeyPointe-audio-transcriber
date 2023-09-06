import sqlite3

CONN = sqlite3.connect('db/convo_database.db')
CURSOR = CONN.cursor()
