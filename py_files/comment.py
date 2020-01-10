from database import DB


class Comment:
    def __init__(self, id, game, message):
        self.id = id
        self.game = game
        self.message = message

    def create(self):
        with DB() as db:
            values = (self.game.id, self.message)
            db.execute(
                'INSERT INTO comments (game_id, message) VALUES (?, ?)',
                values
            )
            return self

    @staticmethod
    def find_by_game(game):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM comments WHERE game_id = ?',
                (post.id,)
            ).fetchall()
            return [Comment(*row) for row in rows]
