import tkinter as tk
import time
from tkinter import *

from generator import Generator

ERR_TEXT = "ERROR: incorrect values"
generator = Generator()


root = tk.Tk()
root.title('Генератор Б/М - ветора')
root.geometry('400x200+300+200')

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


pg_execute_button.bind('<Button-1>', generate_password)
pg_copy_button.bind('<Button-1>', copy)

root.mainloop()