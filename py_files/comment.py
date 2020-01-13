from database import DB

class Comment:
    def __init__(self, id, content, game):
        self.id = id
        self.game = game
        self.content = content
       
    def create(self):
        with DB() as db:
            values = (self.game.id, self.content)
            db.execute(
                'INSERT INTO comments (game_id, content) VALUES (?, ?)',
                values
            )
            return self
    def get_content(self):
        return self.content

    def __repr__(self):
        return "Comment with id: " + self.id 