import sqlite3

from config import DB_NAME
from dao import DB_DIR
from models.User import User


def registration_user(login: str, name: str, password: str):
    """Регистрация пользователя
    :param login: логин пользователя
    :param name: имя пользователя
    :param password: пароль пользователя
    """
    connection = sqlite3.connect(f"{DB_DIR}/{DB_NAME}")
    cursor = connection.cursor()

    user_in_db = cursor.execute(f"SELECT * FROM users WHERE login='{login}';").fetchall()
    if len(user_in_db) != 0:
        return None

    cursor.execute(f"INSERT INTO users (login, name, password) VALUES {login, name, password};")
    connection.commit()

    uid = cursor.lastrowid

    cursor.close()
    connection.close()
    return User(uid=uid, login=login, name=name, password=password)


def login_user(login: str, password: str):
    """Авторизация пользователя
    :param login: логин пользователя
    :param password: пароль пользователя
    """
    connection = sqlite3.connect(f"{DB_DIR}/{DB_NAME}")
    cursor = connection.cursor()

    users = cursor.execute(f"SELECT * FROM users WHERE login='{login}';").fetchall()

    cursor.close()
    connection.close()

    if len(users) != 0 and users[0][3] == password:
        return User(uid=users[0][0], login=users[0][1], name=users[0][2],
                    password=users[0][3], games=str_id_to_list(users[0][4]))
    return None


def update_user(user: User) -> None:
    """Обновляем данные пользователя
    :param user: новый пользователь
    """
    connection = sqlite3.connect(f"{DB_DIR}/{DB_NAME}")
    cursor = connection.cursor()

    gids = ""
    for elem in user.games:
        gids += f";{elem}"
    gids = gids[1:]

    cursor.executescript(f"UPDATE users SET gids='{gids}' WHERE uid='{user.uid}';")
    connection.commit()

    cursor.close()
    connection.close()


def str_id_to_list(sids: str) -> list:
    return list(map(int, sids.split(";"))) if sids is not None else None
