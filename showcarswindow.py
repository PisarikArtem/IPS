from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from config import host,password,user,db_name

class ShowCarWindow:
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


    def create_tree(self):
        try:
            self.carlistreq = f"""SELECT manufacturer, model, price, year FROM usercar WHERE login = '{self.username}'"""
            with self.connectoinlocal.cursor() as self.cursor:
                self.cursor.execute(self.carlistreq)
                self.result = self.cursor.fetchall()
            #print(self.result)
        except Exception as ex:
            print("Ошибка получения машин из БД")
            print(ex)


        self.tree = ttk.Treeview(self.showcarwindow, columns=("Производитель", "Модель", "Цена", "Год"),
                                 show="headings")
        self.tree.pack(fill=BOTH)

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



    def __init__(self,parent,connector, username):
        self.showcarwindow = Toplevel(parent)
        self.connectoinlocal = connector
        self.username = username
        self.showcarwindow.title('Ваши автомобили')
        # размер окна
        self.showcarwindow.resizable(False, False)
        self.showcarwindow.geometry('340x200+400+200')
        self.create_tree()









        self.focus()  # вызов фокуса

    def focus(self):  # фокус на дочернее окно
        self.showcarwindow.grab_set()
        self.showcarwindow.focus_set()
        self.showcarwindow.wait_window()


