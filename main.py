from servicewindow import ServiceWindow
from autorizewindow import MainWindow
import CarCreator
import Car
from config import host,password,user,db_name
import pymysql


try:
    connection_user = pymysql.connect(host=host, port=3306, user=user, password=password, database=db_name,
                                               cursorclass=pymysql.cursors.DictCursor)
    print("База данных подключена успешно")
    # cars = CarCreator.Creator.create_cars_list(50)
    # str = CarCreator.Converter.convert_to_str(cars)
    # lst = str.split(' ')
    # print(lst)
    # man = []
    # mod = []
    # pr = []
    # ye = []
    # for i in range(0,len(lst),4):
    #     man.append(lst[i])
    # for i in range(1,len(lst),4):
    #     mod.append(lst[i])
    # for i in range(2,len(lst),4):
    #     pr.append(lst[i])
    # for i in range(3, len(lst), 4):
    #     ye.append(lst[i])
    #
    # print(man)
    # print(mod)
    # print(pr)
    # print(ye)


    window = MainWindow(connection_user)
    window.run()
except Exception as ex:
    print("Ошибка подключения БД")
    print(ex)





