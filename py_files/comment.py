from database import DB

class Comment:
    def __init__(self, id, content, user, game):
        self.id = id
        self.content = content
        self.user = user
        self.game = game
        
       
    def create(self):
        with DB() as db:
            values = (self.content, self.user.username, self.game.id,)
            db.execute(
                'INSERT INTO comments (content, user_username, game_id) VALUES (?, ?, ?)',
                values
            )
            return self
    @staticmethod
    def find_by_game(game):
        if not game:
            return None
        with DB() as db:
            rows = db.execute('SELECT * FROM comments WHERE game_id = ?', (game.id,) ).fetchall()
            return [Comment(*row) for row in rows]
    @staticmethod
    def find_by_id(id):
        if not id:
            return None
        with DB() as db:
            row = db.execute('SELECT * FROM comments WHERE id = ?', (id,) ).fetchone()
            return Comment(*row)

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM comments WHERE id = ?', (self.id,))
