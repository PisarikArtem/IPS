from tkinter import *
from tkinter import ttk
import json
import re
import CarCreator
import Car
from addcarwindow import AddCarWindow
from showcarswindow import ShowCarWindow
from tkinter import messagebox
from config import host,password,user,db_name
from PIL import Image, ImageTk
import pymysql


class ServiceWindow:
    def create_new_cars(self):
        self.CreatedCarsInDB = f"""SELECT * FROM car"""  # проверяем пустая ли таблица с машинами
        with self.connectoinlocal.cursor() as cursor:
            flag = cursor.execute(self.CreatedCarsInDB)

        if (flag == False):
            self.cars = CarCreator.Creator.create_cars_list(100)  # создаем 100 машин
            self.str = CarCreator.Converter.convert_to_str(self.cars)  # создаем строку из машин
            self.lst = self.str.split(' ')  # создаем список из полученной строки
            self.man = []  # инициализация подсписков для произв, модели, цены и года
            self.mod = []
            self.pr = []
            self.ye = []
            for i in range(0, len(self.lst), 4):  # извлекаем параметры в подсписки
                self.man.append(self.lst[i])
            for i in range(1, len(self.lst), 4):
                self.mod.append(self.lst[i])
            for i in range(2, len(self.lst), 4):
                self.pr.append(self.lst[i])
            for i in range(3, len(self.lst), 4):
                self.ye.append(self.lst[i])

            self.createcars = f""" 
                                    ALTER TABLE car AUTO_INCREMENT = 1;"""  # ставим автоинкремент на 1
            with self.connectoinlocal.cursor() as self.cursor:
                self.cursor.execute(self.createcars)
                self.connectoinlocal.commit()

            for i in range(0, len(self.cars)):
                self.createcars = f"""
                        INSERT INTO car (manufacturer, model, price, year) VALUES ("{self.man[i]}","{self.mod[i]}","{self.pr[i]}","{self.ye[i]}")
                            """
                with self.connectoinlocal.cursor() as self.cursor:
                    self.cursor.execute(self.createcars)
                    self.connectoinlocal.commit()
        else:
            pass

    def create_tree(self):
        try:
            self.carlistreq = f"""SELECT manufacturer, model, price, year FROM car"""
            with self.connectoinlocal.cursor() as self.cursor:
                self.cursor.execute(self.carlistreq)
                self.result = self.cursor.fetchall()
            #print(self.result)
        except Exception as ex:
            print("Ошибка получения машин из БД")
            print(ex)


        self.tree = ttk.Treeview(self.servicewindow, columns=("Производитель", "Модель", "Цена", "Год"),
                                 show="headings")
        self.tree.pack()

        self.tree.column("#1", stretch=NO, width=100)
        self.tree.column("#2", stretch=NO, width=90)
        self.tree.column("#3", stretch=NO, width=100)
        self.tree.column("#4", stretch=NO, width=50)

        self.tree.heading("Производитель", text="Производитель", anchor=W,
                          command=lambda: self.treeview_sort_column('#1', False))
        self.tree.heading("Модель", text="Модель", anchor=W, command=lambda: self.treeview_sort_column('#2', False))
        self.tree.heading("Цена", text="Цена, $", anchor=W, command=lambda: self.treeview_sort_column('#3', False))
        self.tree.heading("Год", text="Год", anchor=W, command=lambda: self.treeview_sort_column('#4', False))

        for i in range(0, len(self.result)):
            self.tree.insert('', i, values=(self.result[i]['manufacturer'], self.result[i]['model'],
                                            self.result[i]['price'], self.result[i]['year']))

    def back_to_reg(self):
        self.servicewindow.destroy()

    def refresh(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.tree.destroy()
        self.create_tree()
        self.get_user_money()
    def search(self, event='<Return>'):
        for char in self.manufacterer_entry.get():
            if char == ' ':
                self.manufacterer_entry.delete(0,'end')
                return messagebox.showinfo('Ошибка', f"В поле производителя не должно быть пробелов")
        for char in self.model_entry.get():
            if char == ' ':
                self.model_entry.delete(0,'end')
                return messagebox.showinfo('Ошибка', f"В поле модели не должно быть пробелов")
        for char in self.price_entry.get():
            if char == ' ':
                self.price_entry.delete(0,'end')
                return messagebox.showinfo('Ошибка', f"В поле цены не должно быть пробелов")
        for char in self.year_entry.get():
            if char == ' ':
                self.year_entry.delete(0, 'end')
                return messagebox.showinfo('Ошибка', f"В поле год не должно быть пробелов")

        self.manufacterer_v = self.manufacterer_entry.get()
        self.model_v = self.model_entry.get()
        self.price_v = self.price_entry.get()
        self.year_v = self.year_entry.get()



        self.searchcars = f"""SELECT manufacturer, model, price, year FROM car WHERE manufacturer LIKE '{self.manufacterer_v}%'
                    AND model LIKE '{self.model_v}%' AND price <= {self.price_v} AND year = {self.year_v} """

        if(self.year_v == ""):
            self.searchcars = f"""SELECT manufacturer, model, price, year FROM car WHERE manufacturer LIKE '{self.manufacterer_v}%'
                    AND model LIKE '{self.model_v}%' AND price <= {self.price_v}"""
        if(self.price_v == ""):
            self.searchcars = f"""SELECT manufacturer, model, price, year FROM car WHERE manufacturer LIKE '{self.manufacterer_v}%'
                                AND model LIKE '{self.model_v}%' AND year = {self.year_v} """
        if(self.year_v == "" and self.price_v == "" ):
            self.searchcars = f"""SELECT manufacturer, model, price, year FROM car WHERE manufacturer LIKE '{self.manufacterer_v}%'
                                            AND model LIKE '{self.model_v}%' """

        with self.connectoinlocal.cursor() as self.cursor:
            self.cursor.execute(self.searchcars)
            self.result_of_search = self.cursor.fetchall()
        print(self.result_of_search)

        [self.tree.delete(i) for i in self.tree.get_children()]

        for i in range(0, len(self.result_of_search)):
            self.tree.insert('', i, values=(self.result_of_search[i]['manufacturer'], self.result_of_search[i]['model'], self.result_of_search[i]['price'], self.result_of_search[i]['year']))

    def treeview_sort_column(self,col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children()]
        if col == '#3':
            l = sorted(l, key=lambda l:int(l[0]),reverse=reverse)
            for index, (val, k) in enumerate(l):
                self.tree.move(k, '', index)
        else:
            l.sort(reverse=reverse)
            for index, (val, k) in enumerate(l):
                self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def add_car_by_admin(self):
        self.addcarwindow = AddCarWindow(self.servicewindow,self.connectoinlocal)
        self.refresh()

    def del_car_by_admin(self):
        for selection in self.tree.selection():
            self.item = self.tree.item(selection)
            print(self.item['values'][1])
            self.delcar = f"""DELETE FROM car WHERE manufacturer = '{self.item['values'][0]}' AND model = '{self.item['values'][1]}' 
            AND price = {self.item['values'][2]} AND year ={self.item['values'][3]} """
            try:
                with self.connectoinlocal.cursor() as self.cursor:
                    self.cursor.execute(self.delcar)
                    self.connectoinlocal.commit()
            except:
                return messagebox.showinfo('Ошибка!', 'Ошибка удаления машин из БД')
        self.refresh()

    def get_user_money(self):
        try:
            self.get_money = f"""SELECT money FROM user WHERE login = "{self.username}";"""
            with self.connectoinlocal.cursor() as self.cursor:
                self.cursor.execute(self.get_money)
                self.result = self.cursor.fetchall()
                for row in self.result:
                    for i in row.keys():
                        self.usermoney = row[i]
            self.main_label = Label(self.servicewindow, text=f'Баланс: {self.usermoney}$', font=('Arial', 10),
                                        justify=CENTER)
            self.main_label.place(x=2, y=22)
        except Exception as ex:
            return messagebox.showinfo("Ошибка","Ошибка получения денежных средств пользователя")

    def sell_a_car(self):
        self.total_price = 0
        for selection in self.tree.selection():
            self.item = self.tree.item(selection)
            self.total_price += self.item['values'][2]
        #print(self.total_price)
        if self.usermoney >= self.total_price:
            for selection in self.tree.selection():
                self.item = self.tree.item(selection)
                self.add_car_into_BD = f""" INSERT INTO usercar (login, manufacturer, model, price, year) VALUES 
                ("{self.username}","{self.item['values'][0]}","{self.item['values'][1]}",{self.item['values'][2]},
                {self.item['values'][3]}); """
                self.delcar = f"""DELETE FROM car WHERE manufacturer = '{self.item['values'][0]}' AND model = '{self.item['values'][1]}' 
                            AND price = {self.item['values'][2]} AND year ={self.item['values'][3]} """
                self.change = f"""UPDATE user SET money={self.usermoney-self.total_price} WHERE login="{self.username}" """
                try:
                    with self.connectoinlocal.cursor() as self.cursor:
                        self.cursor.execute(self.add_car_into_BD)
                        self.cursor.execute(self.delcar)
                        self.cursor.execute(self.change)
                        self.connectoinlocal.commit()
                except:
                    return messagebox.showinfo('Ошибка!', 'Ошибка удаления машин из БД')
        self.refresh()

    def showcars(self):
        self.hadcars = f"""SELECT * FROM usercar WHERE login = '{self.username}'; """
        with self.connectoinlocal.cursor() as cursor:
            self.flag = cursor.execute(self.hadcars)
            print(self.flag)
        if (self.flag > 0):
            self.showcarwindow = ShowCarWindow(self.servicewindow, self.connectoinlocal, self.username)
        else:
            self.emptytable = f"""SELECT * FROM usercar"""
            with self.connectoinlocal.cursor() as cursor:
                self.flag = cursor.execute(self.emptytable)
            if (self.flag == 0):
                self.AI = f""" ALTER TABLE usercar AUTO_INCREMENT = 1;"""
                with self.connectoinlocal.cursor() as self.cursor:
                    self.cursor.execute(self.AI)
                    self.connectoinlocal.commit()
            return messagebox.showinfo("Ошибка",f"У пользователя {self.username} нет машин")


    def __init__(self,username, parent,connector):
        # главное окно приложения
        self.servicewindow = Toplevel(parent)
        self.connectoinlocal = connector
        self.username = username
        # заголовок окна
        self.servicewindow.title('Автосалон')
        # размер окна
        self.servicewindow.geometry('600x500+400+100')
        ###########если список машин пуст то заполняем в БД 100 машин
        self.create_new_cars()
        ##########

        ################ создание таблицы машин

        # можно ли изменять размер окна - нет
        self.servicewindow.resizable(False, False)
        self.font_header = ('Arial', 15)
        self.font_entry = ('Arial', 12)
        self.label_font = ('Arial', 11)
        self.base_padding = {'padx': 10, 'pady': 8}
        self.header_padding = {'padx': 10, 'pady': 12}

        self.main_label = Label(self.servicewindow, text=f'Пользователь: {username}', font=('Arial',10), justify=CENTER)
        # помещаем виджет в окно по принципу один виджет под другим
        self.main_label.place(x=2,y=2)
        self.label = Label(self.servicewindow, text='Автомобили', font=('Arial', 15), justify=CENTER)
        # помещаем виджет в окно по принципу один виджет под другим
        self.label.pack(pady=20)

        self.get_user_money()

        # self.serialized = json.dumps(usermoney)  # преобразованние в строку
        # self.usermoney_str = ' '.join(re.findall(r': ([^: }]+)}', self.serialized))
        # print(self.usermoney_str)



        self.img1 = Image.open('w.png')
        self.img_photo1 = ImageTk.PhotoImage(self.img1)
        self.back_btn = Button(self.servicewindow, image = self.img_photo1, command=self.back_to_reg)
        self.back_btn.place(x=2,y=42)

        self.img2 = Image.open('refpic.png')
        self.img_photo2 = ImageTk.PhotoImage(self.img2)
        self.ref_btn = Button(self.servicewindow, image=self.img_photo2, command=self.refresh)
        self.ref_btn.place(x=446, y=42)



        self.manufacterer_label = Label(self.servicewindow, text="Производитель: ", font=self.label_font)
        self.manufacterer_label.place(x=2, y=350)

        self.manufacterer_entry = Entry(self.servicewindow, bg='#fff', fg='#444', font=self.font_entry)
        self.manufacterer_entry.place(x=122,y=350)

        self.model_label = Label(self.servicewindow, text="Модель: ", font=self.label_font)
        self.model_label.place(x=2, y=380)

        self.model_entry = Entry(self.servicewindow, bg='#fff', fg='#444', font=self.font_entry)
        self.model_entry.place(x=122, y=380)

        self.price_label = Label(self.servicewindow, text="Цена: ", font=self.label_font)
        self.price_label.place(x=2, y=410)

        self.price_entry = Entry(self.servicewindow, bg='#fff', fg='#444', font=self.font_entry)
        self.price_entry.place(x=122, y=410)

        self.year_label = Label(self.servicewindow, text="Год:", font=self.label_font)
        self.year_label.place(x=2, y=440)

        self.year_entry = Entry(self.servicewindow, bg='#fff', fg='#444', font=self.font_entry)
        self.year_entry.place(x=122, y=440)

        self.img3 = Image.open('s.png')
        self.img_photo3 = ImageTk.PhotoImage(self.img3)
        self.search_btn = Button(self.servicewindow, image=self.img_photo3, command=self.search)
        self.search_btn.place(x=280, y=465)
        self.servicewindow.bind('<Return>', self.search)
        self.create_tree()

        if (username == "PisarikArtem"):
            self.img4 = Image.open('plus.png')
            self.img_photo4 = ImageTk.PhotoImage(self.img4)
            self.add_btn = Button(self.servicewindow, image=self.img_photo4, command=self.add_car_by_admin)
            self.add_btn.place(x=386, y=42)
            self.img5 = Image.open('minuss.png')
            self.img_photo5 = ImageTk.PhotoImage(self.img5)
            self.add_btn = Button(self.servicewindow, image=self.img_photo5, command=self.del_car_by_admin)
            self.add_btn.place(x=416, y=42)

        self.sell_btn = Button(self.servicewindow, text="Приобрести автомобиль(-и)", command=self.sell_a_car)
        self.sell_btn.place(x=303, y=300)

        self.showcars_btn = Button(self.servicewindow, text="Ваши автомобили", command=self.showcars)
        self.showcars_btn.place(x=182, y=300)


        self.focus()  # вызов фокуса



    def focus(self):  # фокус на дочернее окно
        self.servicewindow.grab_set()
        self.servicewindow.focus_set()
        self.servicewindow.wait_window()




