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

PASS_COUNT = 3

vs = []
vector = []
passwords = []


root = tk.Tk()
root.title('Генератор Б/М - ветора')
root.geometry('800x400+300+200')

Label(text=f"Длина пароля (1 - {generator.limit()}): ", width=25, height=1).place(x=0, y=0)
Label(text=f"Длина алфавита (1 - {generator.max_len()}): ", width=25, height=1).place(x=0, y=40)

pg_length_text = Text(width=10, height=1)
pg_length_text.place(x=200, y=0)

pg_alphabet_text = Text(width=10, height=1)
pg_alphabet_text.place(x=200, y=40)

pg_execute_button = Button(text='Сгенерировать', width=15, height=1)
pg_execute_button.place(x=0, y=100)

pg_result_label = Label(width=25, height=1)
pg_result_label.place(x=0, y=170)

pg_time_label = Label(width=20, height=1)
pg_time_label.place(x=160, y=100)

pg_copy_button = Button(text="Copy", width=10, height=1)
pg_copy_button.place(x=260, y=150)
pg_copy_button['state'] = 'disabled'

Label(text="Аутентификация", width=15, height=1).place(y=0, x=500)
Label(text="Логин: ", width=15, height=1).place(y=30, x=500)
Label(text="Пароль: ", width=15, height=1).place(y=60, x=500)

reg_execute_button = Button(text='Отправить', width=15, height=1)
reg_execute_button.place(x=500, y=100)

# au_res_label = Label(text="<Auth_res>", width=30, height=1)
# au_res_label.place(y=140, x=500)

mathm.mlt([[0]], [[1]])
mathm.haar_matrix(8)

au_login_text = Text(width=15, height=1)
au_login_text.place(y=30, x=600)

au_password_text = Text(width=15, height=1)
au_password_text.place(y=60, x=600)

Label(text="Регистрация", width=30, height=1).place(x=0, y=250)
Label(text="Логин:", width=10, height=1).place(x=0, y=280)

reg_login_text = Text(width=15, height=1)
reg_login_text.insert("1.0", "user")
reg_login_text.place(x=100, y=280)

sep1 = ttk.Separator(orient=HORIZONTAL)
sep1.pack(fill="x", pady=199)


# reg_ok_button = Button(width=5, height=1, text='Ok')
# reg_ok_button.place(x=250, y=310)

reg_execute_button = Button(width=15, height=1, text='Ввести пароль')
reg_execute_button.place(x=0, y=340)

reg_send_button = Button(width=15, height=1, text='Отправить в БД')
reg_send_button.place(x=350, y=340)

reg_pass_text = Text(width=15, height=1)
reg_pass_text.place(x=190, y=345)

Label(text='Требования:').place(x=550, y=210)
Label(text='1) Пароль не короче 4-х символов').place(x=550, y=230)
Label(text='2) Ввод пароля не менее 3-х раз').place(x=550, y=250)
Label(text='3) Пароли должны совпадать').place(x=550, y=270)
Label(text='4) Логин должен быть уникальным').place(x=550, y=290)
Label(text='5) Логин не может быть пустым').place(x=550, y=310)


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
    # print(vs), print(passwords)
    vector = []


def editor_press(*args):
    vector.append(time.time())


def send(*args):
    login = reg_login_text.get('1.0', END).replace('\n', '')
    global passwords, vs, vector
    if not mathm.all_eq_test(passwords):
        mb.showerror('Не удалось зарегистрировать', 'Пароли не совпадают')
    elif len(vs) < 3:
        mb.showerror('Не удалось зарегистрировать', 'Пароль введён менее трёх раз')
    elif len(vs[0]) < 3:
        mb.showerror('Не удалось зарегистрировать', 'Пароль слишком короткий')
    elif not sql.login_is_unique(login):
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


pg_execute_button.bind('<Button-1>', generate_password)
pg_copy_button.bind('<Button-1>', copy)
reg_execute_button.bind('<Button-1>', input_pass)
reg_pass_text.bind('<KeyPress>', editor_press)
reg_send_button.bind('<Button-1>', send)


root.mainloop()
