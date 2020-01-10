from database import DB
from comment import Comment


class Game:
    def __init__(self, id, name, content, category, xbox, ps, pc, rating, series, developers):
        self.id = id
        self.name = name
        self.developers = developers
        self.content = content
        self.category = category
        self.series = series
        self.xbox = xbox
        self.ps = ps
        self.pc = pc
        self.rating = rating

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM posts').fetchall()
            return [Game(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM games WHERE id = ?',
                (id,)
            ).fetchone()
            return Game(*row)

    @staticmethod
    def find_by_category(category):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM games WHERE category_id = ?',
                (category.id,)
            ).fetchall()
            return [Game(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.name, self.developers, self.content, self.category.id)
            db.execute('''
                INSERT INTO posts (name, developers, content, category_id)
                VALUES (?, ?, ?, ?)''', values)
            return self

    def save(self):
        with DB() as db:
            values = (
                self.id = id
                self.name = name
                self.developers = developers
                self.content = content
                self.category = category
                self.series = series
                self.xbox = xbox
                self.ps = ps
                self.pc = pc
                self.rating = rating
            )
            db.execute(
                '''UPDATE games
                SET name = ?, developers = ?, content = ?, category_id = ? series = ? xbox = ? ps = ? pc = ? rating = ?
                WHERE id = ?''', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM games WHERE id = ?', (self.id,))

    def comments(self):
        return Comment.find_by_game(self)