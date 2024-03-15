import sqlite3

DATABASE = '/data/users.db'


def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            dob DATE NOT NULL,
            email TEXT NOT NULL,
            phoneNumber TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
