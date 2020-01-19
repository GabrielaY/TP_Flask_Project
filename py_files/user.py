from passlib.hash import sha256_crypt

from database import DB

from itsdangerous import (
        TimedJSONWebSignatureSerializer as Serializer,
        BadSignature,
        SignatureExpired
        )

SECRET_KEY = 'ncXZyx5cLR7x1$B^Ybtqp1f!E#dG4H3EN@ioYYKoxx'

class User:
    def __init__(self, id, username, password, admin):
        self.id = id
        self.username = username
        self.password = password
        self.admin = admin

    def create(self):
        with DB() as db:
            values = (self.username, self.password, self.admin)
            db.execute('''
                INSERT INTO users (username, password, admin)
                VALUES (?, ?, ?)''', values)
            return self


    @staticmethod
    def find_by_username(username):
        if not username:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            if row:
                return User(*row)


    @staticmethod
    def hash_password(password):
        return sha256_crypt.encrypt(password)


    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password)





