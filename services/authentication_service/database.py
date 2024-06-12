import sqlite3

DATABASE = '/data/users.db'
CURRENT_USER_ID = 0


def get_connection():
    return sqlite3.connect(DATABASE)


def create_user(username, password, firstName, lastName, dob, email, phoneNumber):
    global CURRENT_USER_ID

    conn = get_connection()
    cursor = conn.cursor()
    CURRENT_USER_ID += 1
    cursor.execute('''INSERT INTO users (id, username, password, firstName, lastName, dob, email, phoneNumber)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (CURRENT_USER_ID, username, password, firstName, lastName, dob, email, phoneNumber))
    conn.commit()
    conn.close()


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_user(username, firstName, lastName, dob, email, phoneNumber):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE users
                      SET firstName=?, lastName=?, dob=?, email=?, phoneNumber=?
                      WHERE username=?''',
                   (firstName, lastName, dob, email, phoneNumber, username))
    conn.commit()
    conn.close()
