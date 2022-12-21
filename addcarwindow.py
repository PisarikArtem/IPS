from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from config import host,password,user,db_name

import customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class AddCarWindow:


    def add_car_to_bd(self, event='<Return>'):
        if (self.price_entry.get() == "" or self.manufacterer_entry.get() == "" or self.model_entry.get()== "" or self.year_entry.get()== ""):
            return messagebox.showinfo('Ошибка', f"Поля не должны быть пустые")

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


        self.manufacterer = self.manufacterer_entry.get()
        self.model = self.model_entry.get()
        self.price = self.price_entry.get()
        self.year = self.year_entry.get()

        self.addcar = f""" INSERT INTO car (manufacturer, model, price, year) VALUES ("{self.manufacterer}","{self.model}",{self.price},{self.year});
                        """
        try:
            with self.connectoinlocal.cursor() as self.cursor:
                self.cursor.execute(self.addcar)
                self.connectoinlocal.commit()
            self.addcarwindow.destroy()
        except:
            return messagebox.showinfo('Ошибка', f"Ошибка добавления машины в БД")
            self.addcarwindow.destroy()





    def __init__(self,parent,connector):
        self.addcarwindow = customtkinter.CTkToplevel(parent)
        self.connectoinlocal = connector
        self.addcarwindow.title('Добавление машины')
        # размер окна
        self.addcarwindow.geometry('310x200+400+200')

        self.addcarwindow.resizable(False, False)
        self.font_header = ('Arial', 15)
        self.font_entry = ('Arial', 13)
        self.label_font = ('Arial', 15)
        self.base_padding = {'padx': 10, 'pady': 8}
        self.header_padding = {'padx': 10, 'pady': 12}

        self.manufacterer_label = customtkinter.CTkLabel(self.addcarwindow, text="Производитель: ", font=self.label_font)
        self.manufacterer_label.place(x=2, y=2)

        self.manufacterer_entry = customtkinter.CTkEntry(self.addcarwindow, font=self.font_entry)
        self.manufacterer_entry.place(x=122, y=2)

        self.model_label = customtkinter.CTkLabel(self.addcarwindow, text="Модель: ", font=self.label_font)
        self.model_label.place(x=2, y=32)

        self.model_entry = customtkinter.CTkEntry(self.addcarwindow, font=self.font_entry)
        self.model_entry.place(x=122, y=32)

        self.price_label = customtkinter.CTkLabel(self.addcarwindow, text="Цена: ", font=self.label_font)
        self.price_label.place(x=2, y=62)

        self.price_entry = customtkinter.CTkEntry(self.addcarwindow, font=self.font_entry)
        self.price_entry.place(x=122, y=62)

        self.year_label = customtkinter.CTkLabel(self.addcarwindow, text="Год:", font=self.label_font)
        self.year_label.place(x=2, y=92)

        self.year_entry = customtkinter.CTkEntry(self.addcarwindow, font=self.font_entry)
        self.year_entry.place(x=122, y=92)

        self.add_btn = customtkinter.CTkButton(self.addcarwindow, text="Добавить машину", command=self.add_car_to_bd)
        self.add_btn.place(x=5,y=132,width=300)

        self.addcarwindow.bind('<Return>', self.add_car_to_bd)



        self.focus()  # вызов фокуса

    def focus(self):  # фокус на дочернее окно
        self.addcarwindow.grab_set()
        self.addcarwindow.focus_set()
        self.addcarwindow.wait_window()
