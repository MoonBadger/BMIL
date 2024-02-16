import db


def login_is_not_exist(login):
    return db.DBManager.aggregate(f"select count(*) from users where login = '{login}'") == 0


def send(login, password, data):
    db.DBManager.change(f"insert into users (login, password, data) values ('{login}', '{password}', '{data}')")


def get_au_data(login):
    res = db.DBManager.select(f"select password, data from users where login = '{login}' ")
    return res[0][0] if res != [] else None, res[0][1] if res != [] else None


def parse(s: str):
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace(' ', '')
    pr = s.split(',')
    res = []
    for val in pr:
        res.append(float(val.replace("'", '')))
    return res

