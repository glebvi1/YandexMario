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

