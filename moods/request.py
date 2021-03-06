import sqlite3
import json
from models import Mood


def get_all_moods():
    with sqlite3.connect("./somethingelse.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.mood
        FROM moods m
        """)
        moods = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            mood = Mood(row['id'], row['mood'])
            moods.append(mood.__dict__)

    return json.dumps(moods)

def get_single_mood(id):
    with sqlite3.connect("./somethingelse.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.mood
        FROM moods m
        WHERE m.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        mood = Mood(data['id'], data['mood'])

        return json.dumps(mood.__dict__)

