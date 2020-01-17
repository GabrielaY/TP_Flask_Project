from database import DB

class Owned(object):

    def __init__(self, id, user, game):

        self.id = id
        self.user = user
        self.game = game

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM owned').fetchall()
            return [Owned(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM owned WHERE id = ?',
                (id,)
            ).fetchone()
            return Owned(*row)

    @staticmethod
    def find_by_user(user):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM owned WHERE user_id = ?',
                (user.id,)
            ).fetchall()
            return [Owned(*row) for row in rows]
    @staticmethod
    def find_by_game(game):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM owned WHERE game_id = ?',
                (game.id,)
            ).fetchall()
            return [Owned(*row) for row in rows]
    def create(self):
        with DB() as db:
            values = (self.user.id, self.game.id,)
            db.execute('''
                INSERT OR REPLACE INTO ratings (score, user_id, game_id)
                VALUES (?, ?, ?)''', values)
        
        return self


