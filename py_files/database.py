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
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS requirements
	(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		CPU TEXT,
		CPU_speed TEXT,
		RAM TEXT,
		OS TEXT,
		video_card TEXT,
		sound_card TEXT,
		free_disc_space TEXT,
		video_RAM TEXT,
		game_id INTEGER UNIQUE,
		FOREIGN KEY(game_id) REFERENCES games(id)
	)
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS owned
	(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_id INTEGER,
		game_id INTEGER,
		UNIQUE(user_id, game_id),
		FOREIGN KEY(user_id) REFERENCES users(id),
		FOREIGN KEY(game_id) REFERENCES games(id)
	)
''')
conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS comments
	(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		content TEXT,
		user_username INTEGER NOT NULL,
		game_id INTEGER NOT NULL,
		FOREIGN KEY(user_username) REFERENCES users(username),
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
