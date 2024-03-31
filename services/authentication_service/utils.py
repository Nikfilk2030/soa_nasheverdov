import hashlib


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def verify_user(database, username: str, password: str) -> bool:
    user = database.get_user(username)

    return user and user[2] == password


class IdGenerator:
    def __init__(self, start=1):
        self.current_id = start - 1

    def get_next_id(self):
        self.current_id += 1
        return self.current_id
