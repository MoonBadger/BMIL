import db


def login_is_unique(login):
    return db.DBManager.aggregate(f"select count(*) from users where login = '{login}'") == 0


def send(login, password, data):
    db.DBManager.change(f"insert into users (login, password, data) values ('{login}', '{password}', '{data}')")

