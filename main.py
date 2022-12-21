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
    window = MainWindow(connection_user)
    window.run()
except Exception as ex:
    print("Ошибка подключения БД")
    print(ex)





