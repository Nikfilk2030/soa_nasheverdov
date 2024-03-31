import sqlite3


def create_users():
    database = '/data/users.db'

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users;")
    cursor.execute('''
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            dob DATE NOT NULL,
            email TEXT NOT NULL,
            phoneNumber TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()


def create_tasks():
    database = '/data/tasks.db'

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS tasks;")
    cursor.execute('''
        CREATE TABLE tasks (
            id integer PRIMARY KEY,
            username text,
            content text,
            date text,
            tag text
        );
    ''')

    conn.commit()
    conn.close()


def create_tables():
    create_users()
    create_tasks()


if __name__ == '__main__':
    create_tables()
