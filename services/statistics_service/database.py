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

