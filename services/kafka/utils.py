class EType:
    Like = 1
    View = 2


def get_type(t: str) -> int:
    if t == 'like':
        return EType.Like
    if t == 'view':
        return EType.View
    raise Exception('unknown EType in get_type')


def is_like(t: int) -> bool:
    return t == EType.Like


def is_view(t: int) -> bool:
    return t == EType.View


def get_db_name(t: int) -> str:
    if is_like(t):
        return 'likes'
    if is_view(t):
        return 'views'
    raise Exception('unknown EType in get_db_name')


def is_duplicate(cursor, db_name, message) -> bool:
    cursor.execute(f"SELECT 1 FROM {db_name} WHERE task_id = ? AND username = ?",
                   (message['task_id'], message['username']))
    return cursor.fetchone() is not None


def insert_into_db(cursor, db_name, message) -> bool:
    cursor.execute(
        f"INSERT INTO {db_name} (task_id, username) VALUES (?, ?)",
        (message['task_id'], message['username']))
    return cursor.rowcount != 0
