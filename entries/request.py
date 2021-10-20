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
            e.tag_ids,
            m.id m_id,
            m.mood
        FROM entries e
        JOIN moods m
            ON m.id = e.mood_id
        """)
        dataset = db_cursor.fetchall()
        entries = []

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'], row['tag_ids'])
            mood = Mood(row['m_id'], row['mood'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)


            db_cursor.execute("""
            SELECT t.id, t.name
            FROM Entries e
            JOIN Entry_tags et on e.id = et.entry_id
            JOIN Tags t on t.id = et.tag_id
            WHERE e.id = ?
            """, (entry.id,))

            tag_set = db_cursor.fetchall()
            for tag_data in tag_set:
                tag = {'id': tag_data['id'], 'name': tag_data['name']}
                entry.tag_ids.append(tag)
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
            e.tag_ids,
            m.id m_id,
            m.mood
        FROM entries e
        JOIN moods m
            on m.id = e.mood_id
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()


        entry = Entry(data['id'], data['concept'], data['entry'],
        data['mood_id'], data['date'], data['tag_ids'])
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
            a.date,
            a.tag_ids
        FROM entries a
        WHERE a.entry LIKE ? 
            OR a.concept LIKE ?
        """, (f'%{search_value}%', f'%{search_value}%' ))
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'], row['tag_ids'])
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

        new_entry['id'] = id

        for tag in new_entry['tag_ids']:
            db_cursor.execute("""
            INSERT INTO Entry_tags(entry_id, tag_id)
            VALUES (?,?)
            """, (id, tag))
        return json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect("./somethingelse.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entries
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?,
                tag_ids = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
                new_entry['moodId'], new_entry['date'], new_entry['tag_ids'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

