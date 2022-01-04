import sqlite3


def save_game(is_win, time, level_number, count_bumps):
    connection = sqlite3.connect("dao/mario.db")
    cursor = connection.cursor()

    cursor.execute(f"DELETE FROM games WHERE level_number={level_number}")
    cursor.execute(f"INSERT INTO games (is_win, time, level_number, count_bumps)"
                   f"VALUES {is_win, time, level_number, count_bumps}")
    connection.commit()

    cursor.close()
    connection.close()


def get_level_number_by_win(is_win):
    connection = sqlite3.connect("dao/mario.db")
    cursor = connection.cursor()

    win_levels = cursor.execute(f"SELECT level_number, time, count_bumps FROM games "
                   f"WHERE is_win={is_win}").fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return win_levels
