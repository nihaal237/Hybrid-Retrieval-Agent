import sqlite3
from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL COLLATE NOCASE,
    type TEXT
);

CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    predicate TEXT NOT NULL,
    object_id INTEGER NOT NULL,
    raw_text TEXT,
    timestamp TEXT,
    FOREIGN KEY(subject_id) REFERENCES entities(id),
    FOREIGN KEY(object_id) REFERENCES entities(id)
);
"""


class GraphMemoryStore:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.GRAPH_DB_PATH
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def get_or_create_entity(self, name: str, type_: str = "unknown") -> int:
        name = name.strip()
        row = self.conn.execute("SELECT id FROM entities WHERE name = ?", (name,)).fetchone()
        if row:
            return row["id"]
        cur = self.conn.execute("INSERT INTO entities (name, type) VALUES (?, ?)", (name, type_))
        self.conn.commit()
        return cur.lastrowid

    def add_relation(self, subject: str, predicate: str, obj: str,
                      subject_type="unknown", object_type="unknown",
                      raw_text="", timestamp=""):
        subj_id = self.get_or_create_entity(subject, subject_type)
        obj_id = self.get_or_create_entity(obj, object_type)
        self.conn.execute(
            """INSERT INTO relations (subject_id, predicate, object_id, raw_text, timestamp)
               VALUES (?, ?, ?, ?, ?)""",
            (subj_id, predicate.lower().strip(), obj_id, raw_text, timestamp),
        )
        self.conn.commit()

    def get_relations_for_entity(self, name: str):
        row = self.conn.execute(
            "SELECT * FROM entities WHERE name LIKE ?", (f"%{name}%",)
        ).fetchone()
        if not row:
            return []
        cur = self.conn.execute(
            """SELECT r.predicate, r.raw_text, r.timestamp,
                      s.name AS subject, o.name AS object
               FROM relations r
               JOIN entities s ON r.subject_id = s.id
               JOIN entities o ON r.object_id = o.id
               WHERE s.id = ? OR o.id = ?
               ORDER BY r.timestamp DESC""",
            (row["id"], row["id"]),
        )
        return [dict(r) for r in cur.fetchall()]
    
    def all_entity_names(self):
        return [row["name"] for row in self.conn.execute("SELECT name FROM entities").fetchall()]
    
    # in GraphMemoryStore
    def counts(self) -> dict:
     e = self.conn.execute("SELECT COUNT(*) c FROM entities").fetchone()["c"]
     r = self.conn.execute("SELECT COUNT(*) c FROM relations").fetchone()["c"]
     return {"entities": e, "relations": r}

    def clear(self):
     self.conn.executescript("DELETE FROM relations; DELETE FROM entities;")
     self.conn.commit()

    
    def search_by_keyword(self, keyword: str):
     like = f"%{keyword}%"
     cur = self.conn.execute(
        """SELECT r.predicate, r.raw_text, r.timestamp,
                  s.name AS subject, o.name AS object
           FROM relations r
           JOIN entities s ON r.subject_id = s.id
           JOIN entities o ON r.object_id = o.id
           WHERE s.name LIKE ? OR o.name LIKE ? OR r.predicate LIKE ?
           LIMIT 10""",
        (like, like, like),
    )
     return [dict(r) for r in cur.fetchall()]