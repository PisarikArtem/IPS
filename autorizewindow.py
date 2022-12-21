# импортируем библиотеку tkinter всю сразу
from tkinter import *
from tkinter import messagebox
import customtkinter
from createwindow import CreateWindow
from servicewindow import ServiceWindow
from config import host,password,user,db_name
import pymysql

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
class MainWindow:


    def clicked_createuser(self):    #создание дочернего окна
        self.window.withdraw()  # скрыть окно
        self.createwindow = CreateWindow(self.window, self.connectionlocal)
        self.window.deiconify()  # показать окно


    def clicked_send(self,event='<Return>'):
        # получаем имя пользователя и пароль
        if (self.username_entry.get() == "" or self.password_entry.get() == ""):
            messagebox.showinfo('Ошибка', 'Пустые поля!')
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
        else:
            self.username = self.username_entry.get()
            self.password = self.password_entry.get()
            # выводим в диалоговое окно введенные пользователем
            self.joinuser = f""" SELECT * FROM user WHERE login = "{self.username}" AND password="{self.password}";
                        """
            # self.connection = pymysql.connect(host=host, port=3306, user=user, password=password, database=db_name,
            #                                   cursorclass=pymysql.cursors.DictCursor)

            with self.connectionlocal.cursor() as self.cursor:
                self.cursor.execute(self.joinuser)
                self.result = self.cursor.fetchall()
                if not self.result:
                    messagebox.showinfo("Ошибка!","Неверный логин или пароль!")
                else:
                    self.window.withdraw() # скрыть окно

                    self.servicewindow = ServiceWindow(self.username,self.window,self.connectionlocal)
                    self.window.deiconify() # показать окно

                    self.username_entry.delete(0,'end')
                    self.password_entry.delete(0, 'end')



    def __init__(self,connection):
        # главное окно приложения
        self.connectionlocal = connection
        self.window = customtkinter.CTk()
        self.window.focus_set()
        # заголовок окна

        self.window.title('Авторизация')
        # размер окна
        self.window.geometry('450x230+400+200')
        # можно ли изменять размер окна - нет
        self.window.resizable(False, False)

        # кортежи и словари, содержащие настройки шрифтов и отступов
        self.font_header = ('Broadway', 30)
        self.font_entry = ('Arial', 13)
        self.label_font = ('Arial', 15)
        self.base_padding = {'padx': 10, 'pady': 8}
        self.header_padding = {'padx': 10, 'pady': 12}


        # обработчик нажатия на клавишу 'Войти'





        # заголовок формы: настроены шрифт (font), отцентрирован (justify), добавлены отступы для заголовка
        # для всех остальных виджетов настройки делаются также
        self.main_label = customtkinter.CTkLabel(self.window, text='Авторизация', font=self.font_header, justify=CENTER, **self.header_padding)
        # помещаем виджет в окно по принципу один виджет под другим
        self.main_label.pack()

        # метка для поля ввода имени
        self.username_label = customtkinter.CTkLabel(self.window, text='Имя пользователя', font=self.label_font , **self.base_padding)
        self.username_label.pack()

        # поле ввода имени
        self.username_entry = customtkinter.CTkEntry(self.window, font=self.font_entry)
        self.username_entry.pack()

        # метка для поля ввода пароля
        self.password_label = customtkinter.CTkLabel(self.window, text='Пароль', font=self.label_font , **self.base_padding)
        self.password_label.pack()

        # поле ввода пароля
        self.password_entry = customtkinter.CTkEntry(self.window,show='*', font=self.font_entry)
        self.password_entry.pack()

        # кнопка отправки формы
        self.send_btn = customtkinter.CTkButton(self.window, text='Войти', command=self.clicked_send)
        self.send_btn.place(x = 130, y = 190, width = 80, height = 26)



        self.createuser_btn = customtkinter.CTkButton(self.window, text='Создать', command=self.clicked_createuser)
        self.createuser_btn.place(x = 235, y = 189, width = 80, height = 26)

        self.window.bind('<Return>', self.clicked_send) #нажатие кнопки ВХОД на клавиатуре через клавишу ENTER
        # запускаем главный цикл окна
    def run(self):
        self.window.mainloop()







