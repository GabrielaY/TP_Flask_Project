import sqlite3

DB_NAME = 'game_catalogue.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        admin INTEGER
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS categories
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS games
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        developers TEXT,
        review TEXT,
        rating REAL,
        release TEXT,
        image TEXT,
        category_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS ratings
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score REAL NOT NULL,
        user_id INTEGER,
        game_id INTEGER,
        UNIQUE(user_id, game_id)
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(game_id) REFERENCES games(id)
    )
''')
conn.commit()


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
