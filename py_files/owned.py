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
    def find_by_game_and_user(game, user):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM owned WHERE game_id = ? AND user_id = ?',
                (game.id, user.id,)
            ).fetchone()
            if row:
                return Owned(*row)
            else:
                return None
    def create(self):
        with DB() as db:
            values = (self.user.id, self.game.id,)
            db.execute('''
                INSERT OR REPLACE INTO owned(user_id, game_id)
                VALUES (?, ?)''', values)
        
        return self
    def delete(self):
        with DB() as db:
            db.execute(''' DELETE FROM owned WHERE id = ?''', (self.id,))



