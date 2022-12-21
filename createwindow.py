from tkinter import *
from tkinter import messagebox
from config import host,password,user,db_name
import random
import pymysql
import customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
class CreateWindow:
    def clicked_send(self, event='<Return>'):
        if (self.username_entry.get() == "" or self.password_entry.get() == "" or self.password_entry2.get() == ""):
            return messagebox.showinfo('Ошибка', 'Пустые поля!')

        if len(self.username_entry.get()) < 5:
            return messagebox.showinfo('Ошибка', f"Логин должен быть не менее 4 символов!")

        if len(self.password_entry.get()) < 7:
            return messagebox.showinfo('Ошибка', f"Пароль должен быть не менее 6 символов!")

        for char in self.username_entry.get():
            if char == ' ':
                self.username_entry.delete(0,'end')
                return messagebox.showinfo('Ошибка', f"В логине не должно быть пробелов!")

        for char in self.password_entry.get():
            if char == ' ':
                return messagebox.showinfo('Ошибка', f"В пароле не должно быть пробелов!")


        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.password2 = self.password_entry2.get()
        if (self.password == self.password2):
            self.CreatedUserInDB = f"""SELECT login FROM user WHERE login = "{self.username}"; """

            with self.connectoinlocal.cursor() as cursor:
                flag = cursor.execute(self.CreatedUserInDB)

            if (flag == False):
                self.createuser = f""" INSERT INTO user (login, password,money) VALUES ("{self.username}","{self.password}","{random.randint(1000, 50000)}")
                """

                with self.connectoinlocal.cursor() as self.cursor:
                    self.cursor.execute(self.createuser)
                    self.connectoinlocal.commit()

                # выводим в диалоговое окно введенные пользователем данные
                # messagebox.showinfo('Заголовок',
                #                     '{username}, {password}'.format(username=self.username, password=self.password))

                self.createwindow.destroy()  # удаление окна
            else:
                 messagebox.showinfo('Ошибка', f"Пользователь с логином {self.username} уже зарегистрирован!")
        else:
            messagebox.showinfo('Ошибка', f"Пароли не совпадают!")



    def __init__(self,parent, connection):
        # главное окно приложения
        self.createwindow = customtkinter.CTkToplevel(parent)
        self.connectoinlocal = connection
        # заголовок окна
        self.createwindow.title('Создание аккаунта')
        # размер окна
        self.createwindow.geometry('400x280+400+200')

        # можно ли изменять размер окна - нет
        self.createwindow.resizable(False, False)
        self.font_header = ('Arial', 15)
        self.font_entry = ('Arial', 13)
        self.label_font = ('Arial', 15)
        self.base_padding = {'padx': 10, 'pady': 8}
        self.header_padding = {'padx': 10, 'pady': 12}


        self.main_label = customtkinter.CTkLabel(self.createwindow, text='Создание аккаунта', font=('Arial',28), justify=CENTER, **self.base_padding)
        # помещаем виджет в окно по принципу один виджет под другим
        self.main_label.pack()

        self.username_label = customtkinter.CTkLabel(self.createwindow, text='Логин', font=self.label_font, **self.base_padding)
        self.username_label.pack()

        self.username_entry = customtkinter.CTkEntry(self.createwindow, font=self.font_entry)
        self.username_entry.pack()

        self.password_label = customtkinter.CTkLabel(self.createwindow, text='Пароль', font=self.label_font , **self.base_padding)
        self.password_label.pack()

        self.password_entry = customtkinter.CTkEntry(self.createwindow, show='*', font=self.font_entry)
        self.password_entry.pack()

        self.password_label2 = customtkinter.CTkLabel(self.createwindow, text='Подтвердите пароль', font=self.label_font, **self.base_padding)
        self.password_label2.pack()

        self.password_entry2 = customtkinter.CTkEntry(self.createwindow, show='*', font=self.font_entry)
        self.password_entry2.pack()

        self.send_btn = customtkinter.CTkButton(self.createwindow, text='Создать пользователя', command=self.clicked_send)
        self.send_btn.pack(pady=10)

        self.createwindow.bind('<Return>', self.clicked_send)  # нажатие кнопки ВХОД на клавиатуре через клавишу ENTER


        self.focus() #вызов фокуса

    def focus(self): # фокус на дочернее окно
        self.createwindow.grab_set()
        self.createwindow.focus_set()
        self.createwindow.wait_window()

