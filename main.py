import tkinter as tk
import time
from tkinter import *

from generator import Generator

ERR_TEXT = "ERROR: incorrect values"
generator = Generator()

PASS_COUNT = 3
vectores = []



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

pg_execute_button = Button(text='Отправить', width=15, height=1)
pg_execute_button.place(x=500, y=100)

# au_res_label = Label(text="<Auth_res>", width=30, height=1)
# au_res_label.place(y=140, x=500)

au_login_text = Text(width=15, height=1)
au_login_text.place(y=30, x=600)

au_password_text = Text(width=15, height=1)
au_password_text.place(y=60, x=600)

Label(text="Регистрация", width=30, height=1).place(x=0, y=250)
Label(text="Логин:", width=10, height=1).place(x=0, y=280)
Label(text="Пароль: ", width=10, height=1).place(x=0, y=310)

reg_login_text = Text(width=15, height=1)
reg_login_text.place(x=100, y=280)

reg_password_text = Text(width=15, height=1)
reg_password_text.place(x=100, y=310)

reg_ok_button = Button(width=5, height=1, text='Ok')
reg_ok_button.place(x=250, y=310)

reg_execute_button = Button(width=15, height=1, text='Отправить', state='disabled')
reg_execute_button.place(x=0, y=340)


def err():
    pg_result_label.config(text=ERR_TEXT)
    pg_time_label.config(text='')
    pg_copy_button['state'] = 'disabled'


def generate_password(*args):
    if pg_execute_button['state'] == 'disabled':
        return
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


pg_execute_button.bind('<Button-1>', generate_password)
pg_copy_button.bind('<Button-1>', copy)

root.mainloop()
