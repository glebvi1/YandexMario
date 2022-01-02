import sqlite3


def save_win_game(is_win, time, level_number):
    connection = sqlite3.connect("dao/mario.db")
    cursor = connection.cursor()

    cursor.execute(f"INSERT INTO games (is_win, time, level_number)"
                   f"VALUES {is_win, time, level_number}")
    connection.commit()

    cursor.close()
    connection.close()


def get_win_level_number():
    connection = sqlite3.connect("dao/mario.db")
    cursor = connection.cursor()

    win_levels = cursor.execute(f"SELECT level_number FROM games "
                   f"WHERE is_win=1").fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return win_levels

