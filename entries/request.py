import sqlite3
import json
from models import Entry, Mood


def get_all_entries():
    with sqlite3.connect("./somethingelse.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.id m_id,
            m.mood
        FROM entries e
        JOIN moods m
            ON m.id = e.mood_id
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])
            mood = Mood(row['m_id'], row['mood'])

            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./somethingelse.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.id m_id,
            m.mood
        FROM entries e
        JOIN moods m
            on m.id = e.mood_id
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()


        entry = Entry(data['id'], data['concept'], data['entry'],
        data['mood_id'], data['date'])
        mood = Mood(data['m_id'], data['mood'])
        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)

def delete_entry(id):
    with sqlite3.connect("./somethingelse.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))

def search_entries(search_value):
    with sqlite3.connect("./somethingelse.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM entries a
        WHERE a.entry LIKE ? 
            OR a.concept LIKE ?
        """, (f'%{search_value}%', f'%{search_value}%' ))
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])
            entries.append(entry.__dict__)

    return json.dumps(entries)

def create_journal_entry(new_entry):
    with sqlite3.connect("./somethingelse.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entries
            ( concept, entry, mood_id, date )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
                new_entry['moodId'], new_entry['date']))

        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id


    return json.dumps(new_entry)