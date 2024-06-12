import sqlite3


def create_users():
    database = '/data/users.db'

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users;")
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
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
            id INTEGER PRIMARY KEY,
            username TEXT,
            content TEXT,
            date TEXT,
            tag TEXT
        );
    ''')

    conn.commit()
    conn.close()


def create_likes():
    database = '/data/stats_data.db'

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS stats_data;")
    cursor.execute('''
        CREATE TABLE stats_data (
            task_id INTEGER PRIMARY KEY, 
            username TEXT, 
            type TEXT
        );
    ''')  # TODO type на всякий случай, мб не нужен

    conn.commit()
    conn.close()


# def create_views():
#     database = '/data/views.db'
#
#     conn = sqlite3.connect(database)
#     cursor = conn.cursor()
#
#     cursor.execute("DROP TABLE IF EXISTS views;")
#     cursor.execute('''
#         CREATE TABLE views (
#             task_id INTEGER PRIMARY KEY,
#             username TEXT,
#             type TEXT
#         );
#     ''')  # TODO type на всякий случай, мб не нужен
#
#     conn.commit()
#     conn.close()


def create_tables():
    create_users()
    create_tasks()
    # create_likes()
    # create_views()


if __name__ == '__main__':
    create_tables()
