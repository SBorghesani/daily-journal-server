import sqlite3
import json
from models import Tags

def get_all_tags():
    with sqlite3.connect('./somethingelse.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM tags t
        """)
        tags = []
        data = db_cursor.fetchall()
        for row in data:
            tag = Tags(row['id'], row['name'])
            tags.append(tag.__dict__)
    
    return json.dumps(tags)