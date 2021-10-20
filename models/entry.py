class Entry():

    def __init__(self, id, concept, entry, mood_id, date, tag_ids):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.date = date
        self.tag_ids = []
        self.mood = None