from database import DB

class Rating(object):

    def __init__(self, id, score, user, game):

        self.id = id
        self.score = score
        self.user = user
        self.game = game

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM ratings').fetchall()
            return [Rating(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM ratings WHERE id = ?',
                (id,)
            ).fetchone()
            return Rating(*row)

    @staticmethod
    def find_by_user(user):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM ratings WHERE user_id = ?',
                (user.id,)
            ).fetchall()
            return [Rating(*row) for row in rows]
    @staticmethod
    def find_by_game(game):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM ratings WHERE game_id = ?',
                (game.id,)
            ).fetchall()
            return [Rating(*row) for row in rows]
    def create(self):
        with DB() as db:
            values = (self.score, self.user.id, self.game.id,)
            db.execute('''
                INSERT OR REPLACE INTO ratings (score, user_id, game_id)
                VALUES (?, ?, ?)''', values)
    
        return self

    def save(self):
        with DB() as db:
            values = (
                self.score,
                self.user.id,
                self.game.id
            )
            db.execute(
                '''UPDATE games
                SET score = ?, user_id = ?, game_id = ?
                WHERE id = ?''', values)
            return self
