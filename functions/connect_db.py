
import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "music.db")
conn = sqlite3.connect(db_path)

def get_connection():
    
    return conn