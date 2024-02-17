import tkinter as tk
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import sql_builder as sql

import mathm
from generator import Generator

ERR_TEXT = "ERROR: incorrect values"
generator = Generator()

vs = []
vector = []
passwords = []
read_vct = []


root = tk.Tk()
root.title('БМИЛ')
root.geometry('800x400+300+200')

Label(text="Генератор паролей").place(x=0, y=0)
Label(text=f"Длина пароля (1 - {generator.limit()}): ", width=25, height=1).place(x=0, y=30)
Label(text=f"Длина алфавита (1 - {generator.max_len()}): ", width=25, height=1).place(x=0, y=60)

pg_length_text = Text(width=15, height=1)
pg_length_text.place(x=200, y=30)

pg_alphabet_text = Text(width=15, height=1)
pg_alphabet_text.place(x=200, y=60)

pg_execute_button = Button(text='Сгенерровать', width=15, height=1)
pg_execute_button.place(x=0, y=150)

pg_result_label = Label(width=25, height=1)
pg_result_label.place(x=0, y=100)

pg_time_label = Label(width=20, height=1)
pg_time_label.place(x=160, y=100)

pg_copy_button = Button(text="Копировать в буфер", width=15, height=1)
pg_copy_button.place(x=200, y=150)
pg_copy_button['state'] = 'disabled'

Label(text="Аутентификация", width=15, height=1).place(y=0, x=500)
Label(text="Логин: ", width=15, height=1).place(y=30, x=500)
Label(text="Пароль: ", width=15, height=1).place(y=60, x=500)

au_execute_button = Button(text='Войти', width=15, height=1)
au_execute_button.place(x=500, y=100)

au_login_text = Text(width=15, height=1)
au_login_text.place(y=30, x=600)

au_password_text = Text(width=15, height=1)
au_password_text.place(y=60, x=600)

Label(text="Регистрация", height=1).place(x=10, y=210)
Label(text="Логин:", width=10, height=1).place(x=0, y=250)

reg_login_text = Text(width=15, height=1)
# reg_login_text.insert("1.0", "user")
reg_login_text.place(x=100, y=250)

sep1 = ttk.Separator(orient=HORIZONTAL)
sep1.pack(fill="x", pady=199)


# reg_ok_button = Button(width=5, height=1, text='Ok')
# reg_ok_button.place(x=250, y=310)

reg_execute_button = Button(width=15, height=1, text='Ввести пароль')
reg_execute_button.place(x=350, y=250)

reg_send_button = Button(width=15, height=1, text='Отправить в БД')
reg_send_button.place(x=350, y=340)

reg_cancel_button = Button(width=15, height=1, text='Сброс')
reg_cancel_button.place(x=350, y=295)

reg_pass_text = Text(width=15, height=1)
reg_pass_text.place(x=100, y=295)

Label(text="Пароль: ").place(x=15, y=295)
Label(text='Требования для регистрации:').place(x=550, y=210)
Label(text='1) Пароль не короче 5-ти символов').place(x=550, y=250)
Label(text='2) Ввод пароля не менее 3-х раз').place(x=550, y=270)
Label(text='3) Пароли должны совпадать').place(x=550, y=290)
Label(text='4) Логин должен быть уникальным').place(x=550, y=310)
Label(text='5) Логин не может быть пустым').place(x=550, y=330)


def err():
    pg_result_label.config(text=ERR_TEXT)
    pg_time_label.config(text='')
    pg_copy_button['state'] = 'disabled'


def generate_password(*args):
    try:
        pass_len = int(pg_length_text.get("1.0", END))
        alph_len = int(pg_alphabet_text.get("1.0", END)) - 1
        if ((0 < pass_len <= generator.limit())
                and (0 <= alph_len < generator.max_len())):
            start = time.time()
            password = generator.generate_pass(pass_len, alph_len)
            dtime = time.time() - start
            pg_result_label.config(text=f"Password: {password}")
            pg_time_label.config(text=f"time: {dtime * 1000:.3f} ms")
            pg_copy_button['state'] = 'normal'
        else:
            err()
    except:
        err()


def copy(*args):
    root.clipboard_clear()
    root.clipboard_append(pg_result_label['text'].split(' ')[1])


def input_pass(*args):
    global vs, current_pass_num, passwords, inp_flag, vector
    passwords.append(reg_pass_text.get("1.0", END).replace("\n", ''))
    reg_pass_text.replace('1.0', END, '')
    vs.append(mathm.normalize(vector))
    vector = []


def editor_press(*args):
    vector.append(time.time())


def au_editor_press(*args):
    global read_vct
    if read_vct == None:
        read_vct = []
    read_vct.append(time.time())


def reset(*args):
    global vs, current_pass_num, passwords, inp_flag, vector
    vs = []
    passwords = []
    vector = []
    reg_pass_text.replace('1.0', END, '')


def __send(*args):
    try:
        send(args)
    except:
        mb.showerror('Ошибка', 'Проверьте корректность введёных данных')


def send(*args):
    login = reg_login_text.get('1.0', END).replace('\n', '')
    global passwords, vs, vector
    if not mathm.all_eq_test(passwords):
        mb.showerror('Не удалось зарегистрировать', 'Пароли не совпадают')
    elif len(vs) < 3:
        mb.showerror('Не удалось зарегистрировать', 'Пароль введён менее трёх раз')
    elif len(vs[0]) < 3:
        mb.showerror('Не удалось зарегистрировать', 'Пароль слишком короткий')
    elif not sql.login_is_not_exist(login):
        mb.showerror('Не удалось зарегистрировать', 'Такой логин уже существует')
    elif login == '':
        mb.showerror('Не удалось зарегистрировать', 'Логин не должен быть пустым')
    else:
        res_vect = mathm.average_of_arrays(vs)
        sql.send(login, passwords[0], str(res_vect))
        mb.showinfo('Ок', 'Регистрация успешна!')
    vs = []
    passwords = []
    vector = []


def __auth(*args):
    global read_vct
    try:
        auth(args)
    except:
        mb.showerror('Не удалось войти', 'Несовпадение биометрических параметров')
        read_vct = None


def auth(*args):
    global read_vct
    login = au_login_text.get('1.0', END).replace('\n', '')
    password = au_password_text.get('1.0', END).replace('\n', '')

    if login == '' or password == '':
        mb.showerror('Не удалось войти', 'Логин и пароль не могут быть пустыми')
    elif sql.login_is_not_exist(login):
        mb.showerror('Не удалось войти', 'Неизвестный логин')
    else:
        real_password, real_data = sql.get_au_data(login)

        if password != real_password:
            mb.showerror('Не удалось войти', 'Неверный пароль')
        else:
            data = mathm.normalize(read_vct)
            parsed_rd = sql.parse(real_data)
            cm = mathm.cosine_similarity(parsed_rd, data)
            if cm < 0.99:
                mb.showerror('Не удалось войти', 'Несовпадение биометрических параметров')
            else:
                mb.showinfo('Ок', 'Вход успешен')

    read_vct = None
    au_password_text.replace("1.0", END, '')


pg_execute_button.bind('<Button-1>', generate_password)
pg_copy_button.bind('<Button-1>', copy)
reg_execute_button.bind('<Button-1>', input_pass)
reg_pass_text.bind('<KeyPress>', editor_press)
reg_send_button.bind('<Button-1>', __send)
reg_cancel_button.bind('<Button-1>', reset)
au_password_text.bind('<KeyPress>', au_editor_press)
au_execute_button.bind('<Button-1>', __auth)


root.mainloop()
