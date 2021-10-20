import sqlite3
import json
from models import Entry_tags


def get_all_entry_tags():
    with sqlite3.connect("./somethingelse.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Select
            et.id,
            et.entry_id,
            et.tag_id
        FROM entry_tags et
        """)
        entry_tags = []
        data = db_cursor.fetchall()
        for row in data:
            entry_tag = Entry_tags(row['id'], row['entry_id'], row['tag_id'])

            entry_tags.append(entry_tag.__dict__)

    return json.dumps(entry_tags)