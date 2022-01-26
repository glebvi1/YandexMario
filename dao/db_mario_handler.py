import sqlite3
from config import DB_NAME
from dao import DB_DIR


def save_game(is_win: bool, time: str, level_number: int, count_money: int) -> None:
    """Сохранение игры в БД
    :param is_win: выиграл ли уровень
    :param time: время, затраченное на уровень
    :param level_number: номер уровня
    :param count_money: количество собранных монеток
    """
    connection = sqlite3.connect(f"{DB_DIR}/{DB_NAME}")
    cursor = connection.cursor()

    cursor.execute(f"DELETE FROM games WHERE level_number={level_number}")
    cursor.execute(f"INSERT INTO games (is_win, time, level_number, count_money)"
                   f"VALUES {is_win, time, level_number, count_money}")
    connection.commit()

    cursor.close()
    connection.close()


def get_level_number_by_win(is_win: bool):
    """Возращаем выигранные уровни, если is_win=True, иначе - проигранные
    :param is_win: True = выигранные; False = проигранные
    """
    connection = sqlite3.connect(f"{DB_DIR}/{DB_NAME}")
    cursor = connection.cursor()

    win_levels = cursor.execute(f"SELECT level_number, time, count_money FROM games "
                   f"WHERE is_win={is_win}").fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    return win_levels
