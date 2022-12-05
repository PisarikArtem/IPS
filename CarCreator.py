import random
from Car import Car


class Creator:
    MARKS = ("Toyota", "Mitsubishi", "Audi", "BMW", "Renault")
    MODELS_Toyota = ("Corolla","Camry", "Highlander", "LandCruiser")
    MODELS_Mitsubishi = ("Outlander", "Lancer", "ASX", "PajeroSport")
    MODELS_Audi = ("TT", "R8", "Q7", "A6", "100C4")
    MODELS_BMW = ("i3", "i8", "M1", "M8", "X5")
    MODELS_Renault = ("Logan", "Scenic3", "Megane", "Duster")

    MIN_YEAR = 1990
    MAX_YEAR = 2021

    MIN_PRICE = 1000
    MAX_PRICE = 30000

    MIN_HP = 100
    MAX_HP = 700

    @staticmethod
    def create_cars_list(amount):
        ls = []

        for _ in range(amount):
            brand = random.choice(Creator.MARKS)
            if brand == "Toyota":
                model = random.choice(Creator.MODELS_Toyota)
            elif brand == "Mitsubishi":
                model = random.choice(Creator.MODELS_Mitsubishi)
            elif brand == "Audi":
                model = random.choice(Creator.MODELS_Audi)
            elif brand == "BMW":
                model = random.choice(Creator.MODELS_BMW)
            else: model = random.choice(Creator.MODELS_Renault)
            year = random.randint(Creator.MIN_YEAR, Creator.MAX_YEAR)
            price = random.randint(Creator.MIN_PRICE, Creator.MAX_PRICE)
            ls.append(Car(brand, model, price, year))


        return ls

class Converter:
    def convert_to_str(ls):
        if isinstance(ls, list):
            message = ""
            counter = 1
            for car in ls:
                message += str(car) + ' '
                counter += 1
            return message
        return 'ERROR'