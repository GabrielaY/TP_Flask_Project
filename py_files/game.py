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
    def sort_by_rating():
        with DB() as db:
            rows = db.execute('''
                SELECT game_id, name, developers, review, rating, release, image, category_id  FROM ratings JOIN games  ON ratings.game_id = games.id GROUP BY game_id ORDER BY avg(score) DESC;
            ''').fetchall()
            return [Game(*row) for row in rows]
    @staticmethod
    def sort_by_alp():
        with DB() as db:
            rows = db.execute('''
                SELECT * FROM games ORDER BY name ASC;
            ''').fetchall()
            return [Game(*row) for row in rows]
    @staticmethod
    def sort_by_newest():
        with DB() as db:
            rows = db.execute('''   
                SELECT * FROM games ORDER BY release DESC;
            ''').fetchall()
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
    def calc_rating(id):
        with DB() as db:
            row = db.execute(
                'SELECT avg(score) as avg_score FROM ratings WHERE game_id = ?',
                (id,)
            ).fetchone()
            
            return row[0]

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


