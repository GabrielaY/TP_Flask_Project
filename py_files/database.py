import sqlite3

DB_NAME = 'game_catalogue.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS gamecategories
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS games
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        developers TEXT,
        series TEXT,
        ps INTEGER, #There's no boolean data type in sqlite3, it's stored in integers (1 = True, 0 = False)
        xbox INTEGER,
        pc INTEGER,
        release TEXT,
        requirements TEXT,
        rating REAL, #float data type in sqlite3
        content TEXT,
        category_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES gamecategories(id)
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS comments
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        message TEXT,
        FOREIGN KEY(game_id) REFERENCES games(id)
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        email TEXT UNIQUE NOT NULL,
        
    )
''')
conn.commit()


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()