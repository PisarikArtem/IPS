class Car:
    car_counter = 0

    def __init__(self, brand, model, price, year):
        self.__brand = brand
        self.__model = model
        self.__year = year
        self.__price = price
        Car.car_counter += 1

    @property
    def brand(self):
        return self.__brand

    @property
    def model(self):
        return self.__model

    @property
    def price(self):
        return self.__price

    @property
    def year(self):
        return self.__year

    @brand.setter
    def brand(self, brand):
        self.__brand = brand

    @model.setter
    def model(self, model):
        self.__model = model

    @price.setter
    def price(self, price):
        if isinstance(price, int) and price >= 0:
            self.__price = price
        else:
            self.__price = 0

    @year.setter
    def year(self, year):
        if isinstance(year, int) and year >= 1:
            self.__year = year
        else:
            self.__year = 0


    def __del__(self):
        Car.car_counter -= 1

    def __str__(self):
        return f"{self.__brand} {self.__model} {self.__price} {self.__year}"




