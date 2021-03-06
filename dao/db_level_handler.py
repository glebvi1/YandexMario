import sqlite3
from config import DB_NAME
from dao import DB_DIR


def save_game(is_win: bool, time: str, level_number: int, count_money: int, level_id: int) -> int:
    """Сохранение игры в БД
    :param is_win: выиграл ли уровень
    :param time: время, затраченное на уровень
    :param level_number: номер уровня
    :param count_money: количество собранных монеток
    """
    connection = sqlite3.connect(f"{DB_DIR}/{DB_NAME}")
    cursor = connection.cursor()

    if level_id is not None:
        cursor.execute(f"UPDATE games SET is_win={is_win}, time='{time}', level_number={level_number},"
                       f" count_money={count_money} WHERE gid={level_id}")
    else:
        cursor.execute(f"INSERT INTO games (is_win, time, level_number, count_money)"
                       f"VALUES {is_win, time, level_number, count_money}")

    connection.commit()

    gid = cursor.lastrowid

    cursor.close()
    connection.close()
    return gid


def get_level_by_ids(list_id: list):
    connection = sqlite3.connect(f"{DB_DIR}/{DB_NAME}")
    cursor = connection.cursor()

    levels = []
    for gid in list_id:
        levels.append(cursor.execute(f"SELECT level_number, time, count_money, is_win FROM games "
                       f"WHERE gid={gid}").fetchone())
    connection.commit()

    cursor.close()
    connection.close()
    return levels
