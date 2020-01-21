from database import DB

class Requirements(object):

    def __init__(self, id, cpu, cpu_speed, ram, os, video_card, sound_card, free_disc_space, video_ram, game):

        self.id = id
        self.cpu = cpu
        self.cpu_speed = cpu_speed
        self.ram = ram
        self.os = os
        self.video_card = video_card
        self.sound_card = sound_card
        self.free_disc_space = free_disc_space
        self.video_ram = video_ram
        self.game = game

    

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM requirements WHERE id = ?',
                (id,)
            ).fetchone()
            return Requirements(*row)

    @staticmethod
    def find_by_game(game):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM requirements WHERE game_id = ?',
                (game.id,)
            ).fetchone()
            return Requirements(*row)
    def create(self):
        with DB() as db:
            values = (self.id, self.cpu, self.cpu_speed, self.ram, self.os, self.video_card, self.sound_card, self.free_disc_space, self.video_ram, self.game.id,)
            a = db.execute('''
                INSERT OR REPLACE INTO requirements (id, cpu, cpu_speed, ram, os, video_card, sound_card, free_disc_space, video_ram, game_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)
        return self

    
