from database import DB


class Game:
    def __init__(self, id, name, developers, review, rating, release, image, category):
        self.id = id
        self.name = name
        self.developers = developers
        self.review = review
        self.release = release
        self.rating = rating
        self.image = image
        self.category = category

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM games').fetchall()
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
            values = (self.name, self.developers, self.review, self. rating, self.image, self.category.id)
            db.execute('''
                INSERT INTO games (name, developers, review, rating, release, image, category_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
            return self

    def save(self):
        with DB() as db:
            values = (
                self.name,
                self.developers,
                self.review,
                self.release,
                self.rating,
                self.category.id,
                self.image,
                self.id
            )
            db.execute(
                '''UPDATE games
                SET name = ?, developers = ?, review = ?, rating = ?, release = ?, image = ?, category_id = ?
                WHERE id = ?''', values)
            return self


    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM games WHERE id = ?', (self.id,))


