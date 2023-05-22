# Команди необхідні для встановлення бібліотек, що використовуються в цьому файлі
# pip install Flask
# pip install Flask-RESTful
from datetime import datetime
from flask import Flask
from flask_restful import Api, Resource
import os.path
import json
# Назви файлів для бази даних
filename = "Database.json" # Основна база даних
fiksturefilename = "Databaseficsture.json" # Резервна база даних
# Змінна де зберігаються замовлення
orders = {}
# Перевірка на існування файлу
if os.path.isfile(filename):
    with open(filename, "r") as file:
        orders = json.load(file)

app = Flask("EShop")
api = Api()

discount = 0.2 # Знижка
# Функція порівняння двох дат. Визначає чи є різниця в датах менше місяця
def compare_date(date1, date2):
    if abs((date1 - date2).total_seconds()) <= 2592000:
        return True
    else: return False

# Класи
class Product: # Продукт
    def __init__(self, name, price, date):
        self.name = name
        self.price = price
        self.date = date

class Casser: # Касир
    def __init__(self, name):
        self.name = name
    def make_order(self, prod): # Створення замовлення
        dis = 0
        if not compare_date(datetime.now(), datetime.strptime(prod.date, '%d-%m-%Y')):
            dis = discount*prod.price
        order = {"Casser name": self.name, "Product name": prod.name, "Creation date": str(prod.date), "Order date": str(datetime.now().strftime('%d-%m-%Y')), "Price": prod.price, "Discount": dis, "Total": prod.price - dis, "Status": "On Service"}
        orders[len(orders)+1] = order
        return order
    def gen_check(self, order): # Створення чеку
        check = {"Product name": order["Product name"], "Creation date": order["Creation date"], "Check date": str(datetime.now().strftime('%d-%m-%Y')), "Price": order["Price"], "Discount": order["Discount"], "Total": order["Price"] - order["Discount"]}
        return check
    def change_status(self, order): # Зміна статусу на "Сплачено"
        order["Status"] = "Paid"
        return order

class Consultant: # Консультант
    def __init__(self, name):
        self.name = name
    def check_orders(self): # Перевірка замовлень. На відміну від бухгалтера бачить лише замовлення зі статусом "Обслуговується"
        res = {}
        for order in orders:
            if orders[order]['Status'] == "On Service":
                res[len(res)+1] = orders[order]
        return res
    def change_status(self, order): # Зміна статусу на "Виконано"
        order["Status"] = "Done"
        return order

class Booker: # Бухгалтер
    def __init__(self, name):
        self.name = name
    def check_orders(self, dates): # перевірка замовлень. Можлива перевірка за датами або перевірка всіх замовлень
        if dates == "0": # Вводимий параметр, при якому перевіряються всі замовлення
            return orders
        dates = dates.split(',') # В стандартному випадку дати перевірки розділяються комою. Якщо є бажання перевірити одну дату, слід ввести її двічі через кому
        res = {}
        for order in orders:
            if datetime.strptime(orders[order]["Order date"], '%d-%m-%Y') >= datetime.strptime(dates[0], '%d-%m-%Y') and datetime.strptime(orders[order]["Order date"], '%d-%m-%Y') <= datetime.strptime(dates[1], '%d-%m-%Y'):
                res[len(res)+1] = orders[order]
        return res
# Ініціювання основних змінних. В даній програмі не має можливості створення об'єктів класу самотужки.
casser = Casser("Lesha")
consultant = Consultant("Pasha")
booker = Booker("Sveta")
products = []
products.append(Product("tv", 3200, datetime.now().strftime('%d-%m-%Y')))
products.append(Product("2", 3600, datetime.now().strftime('%d-%m-%Y')))
products.append(Product("phone", 50000, datetime(2022, 4, 24).strftime('%d-%m-%Y')))

class Main(Resource):
    
    def get(self, classs, method, param): # Головна функція обробки запитів. Приймає 3 параметри: Клас, метод і параметр
        global orders
        if classs == "Casser":
            if method == "make_order":
                for prod in products:
                    if prod.name == param:
                        for order in orders:
                            if orders[order]["Product name"] == param:
                                return "Order with such name is already exsit"
                        res = casser.make_order(prod)
                
            elif method == "gen_check":
                for order in orders:
                    if orders[order]["Product name"] == param:
                        res = casser.gen_check(orders[order])
                
            elif method == "change_status":
                for order in orders:
                    if orders[order]["Product name"] == param:
                        res = casser.change_status(orders[order])
                
        elif classs == "Consultant":
            if method == "check_orders":
                res = consultant.check_orders()
                if len(res) == 0:
                    res = "Не має замовлень"
                
            elif method == "change_status":
                for order in orders:
                    if orders[order]["Product name"] == param:
                        res = consultant.change_status(orders[order])
                
        elif classs == "Booker":
            if method == "check_orders":
                res = booker.check_orders(param)
        elif classs == "0": # Обробка запиту на створення резервного файлу бази даних
            if method == "0":
                with open(fiksturefilename, 'w') as file:
                    json.dump(orders, file)
                    res = "Файл збережено"
            elif method == "1": # Завантаження резервного файлу в основний
                with open(fiksturefilename, 'r') as file:
                    orders = json.load(file)
                    res = "Сейв завантажено"
        with open(filename, 'w') as file: # після кожної обробки данні в файлі бази данил перезаписуються
            json.dump(orders, file)
        return res
# Реалізація запуску серверу
api.add_resource(Main, "/api/<string:classs>/<string:method>/<string:param>")
api.init_app(app)
app.run(debug=False, port= 3000, host="localhost")
