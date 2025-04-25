import psycopg2
import csv

def connect():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="Pg_sql_2025_pp2",  
        host="localhost",
        port="5432"
    )

def insert_from_csv():
    with open(r'C:\My Web Sites\pp2\Lab_10\phonebook.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # пропуск заголовка
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)",
                (row[0], row[1])
            )
    print("Данные из CSV успешно добавлены.")

def insert_from_input():
    name = input("Введите имя: ")
    phone = input("Введите номер телефона: ")
    cur.execute(
        "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)",
        (name, phone)
    )
    print("Данные успешно добавлены вручную.")

# Функция для обновления данных
def update_data():
    print("Выберите, что хотите обновить:")
    print("1 — Обновить имя")
    print("2 — Обновить номер телефона")
    choice = input("Ваш выбор: ")

    if choice == "1":
        # Обновляем имя
        old_name = input("Введите старое имя: ")
        new_name = input("Введите новое имя: ")
        cur.execute(
            "UPDATE phonebook SET first_name = %s WHERE first_name = %s",
            (new_name, old_name)
        )
        print(f"Имя пользователя {old_name} обновлено на {new_name}.")
    
    elif choice == "2":
        # Обновляем телефон
        name = input("Введите имя пользователя: ")
        new_phone = input("Введите новый номер телефона: ")
        cur.execute(
            "UPDATE phonebook SET phone_number = %s WHERE first_name = %s",
            (new_phone, name)
        )
        print(f"Номер телефона для {name} обновлен на {new_phone}.")
    
    else:
        print("Неверный выбор!")

#Добавили функцию query_data() для получения данных с фильтрами
def query_data():
    print("Выберите фильтр для поиска:")
    print("1 — Показать всех пользователей")
    print("2 — Найти по имени")
    print("3 — Найти по номеру телефона")
    print("4 — Найти по части имени")

    choice = input("Ваш выбор: ")

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
        results = cur.fetchall()
    elif choice == "2":
        name = input("Введите имя для поиска: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
        results = cur.fetchall()
    elif choice == "3":
        phone = input("Введите номер телефона для поиска: ")
        cur.execute("SELECT * FROM phonebook WHERE phone_number = %s", (phone,))
        results = cur.fetchall()
    elif choice == "4":
        part = input("Введите часть имени: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", ('%' + part + '%',))
        results = cur.fetchall()
    else:
        print("Неверный выбор!")
        return

    # Выводим результат
    if results:
        print("Результаты поиска:")
        for row in results:
            print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    else:
        print("Ничего не найдено.")

#Добавили возможность удалять записи из таблицы
def delete_data():
    print("Выберите способ удаления:")
    print("1 — Удалить по имени")
    print("2 — Удалить по номеру телефона")

    choice = input("Ваш выбор: ")

    if choice == "1":
        name = input("Введите имя пользователя для удаления: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
        print(f"Пользователь(и) с именем '{name}' удалён(ы).")
    
    elif choice == "2":
        phone = input("Введите номер телефона для удаления: ")
        cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone,))
        print(f"Пользователь с номером '{phone}' удалён.")
    
    else:
        print("Неверный выбор!")

# Подключение
conn = connect()
cur = conn.cursor()

print("Выберите способ добавления данных:")
print("1 - Загрузить из CSV")
print("2 - Ввести вручную")
print("3 - Обновить данные")
print("4 - Найти данные")
print("5 - Удалить данные")

choice = input("Ваш выбор: ")

if choice == "1":
    insert_from_csv()
elif choice == "2":
    insert_from_input()
elif choice =="3":
    update_data()
elif choice =="4":
    query_data()
elif choice =="5":
    delete_data()
else:
    print("Неверный выбор!")

conn.commit()
cur.close()
conn.close()