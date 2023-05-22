# Команда необхідні для встановлення бібліотек, що використовуються в цьому файлі
# python -m pip install requests
import requests

while(True): # Тут реалізоване просте меню. Працює поки програма не видасть помилку або ви не вийдете
    
    choice = input("1. Створити запит\n2. Зберегди поточні данні бази даних\n3. Завантажити дані з сейву\n4. Вийти\n")
    if choice == "1":
        classs = ""
        a = input("Оберіть працівника:\n1. Касир\n2. Консультант\n3. Бухгалтер\n")
        if a == "1":
            classs = "Casser"
            b = input("Оберіть дію:\n1. Прийняти замовлення\n2. Генерування чеку\n3. Зміна статусу\n")
            if b == "1":
                method = "make_order"
                param = input("Введіть назву продукта, на який оформлюєте замовлення\n")
            elif b == "2":
                method = "gen_check"
                param = input("Введіть назву продукта, на який оформлюєте чек\n")
            elif b == "3": 
                method = "change_status"
                param = input("Введіть назву продукта, статус якого хочете змінити\n")
            else:
                print("Обрана дія не існує")
        elif a == "2":
            classs = "Consultant"
            b = input("Оберіть дію:\n1. Перевірити замовлення\n2. Зміна статусу\n")
            if b == "1":
                method = "check_orders"
                param = "0"
            elif b == "2":
                method = "change_status"
                param = input("Введіть назву продукта, статус якого хочете змінити\n")
            else:
                print("Обрана дія не існує")
        elif a == "3":
            classs = "Booker"
            b = input("Оберіть дію:\n1. Перевірити замовлення\n")
            if b == "1":
                method = "check_orders"
                param = input("Введіть дати через кому у форматі d-m-Y(18-07-1992) для перегляду замовлень за датами, або 0 для перевірки всіх замовлень\n")
            else:
                print("Обрана дія не існує")
        else:
            print("Обрана дія не існує")
        if classs != "": # Протягом обирання дій ви вводите параметри необхідні для надсилання запиту. Змінну param заповнюєте ви самі, тому вона може спричинити помилку при її обробці
            address = "http://localhost:3000/api/"+classs+"/"+method+"/"+param
            res = requests.get(address) # Посилання запиту й очікування відповіді
            print(res.json()) # Вивід результату запиту
    # Реалізація резервного копіювання та завантаження з резерву бази даних
    elif choice == "2": # Копіювання
        res = requests.get("http://localhost:3000/api/0/0/0")
        print(res.json())
    elif choice == "3":# Завантаження
        res = requests.get("http://localhost:3000/api/0/1/0")
        print(res.json())
    elif choice == "4": # Вихід
        break