import hashlib


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def verify_user(database, username: str, password: str) -> bool:
    user = database.get_user(username)

    return user and user[2] == password
