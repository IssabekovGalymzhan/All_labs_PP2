import psycopg2
import csv
from tabulate import tabulate

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="TEMA2007", port=5432)
cur = conn.cursor()

# Создание таблицы phonebook
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL
    );
""")
conn.commit()

# Вставка данных из CSV
filepath = r'C:\Users\Admin\Git\Programming-Principles-2\lab10.py\contacts.csv'
def insert_data_from_csv(filepath):
    try:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (row[0], row[1], row[2]))
            conn.commit()
            print("Data inserted from CSV file.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error: {e}")

# Вставка данных с консоли
def insert_data_from_console():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone number: ")
    cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
    conn.commit()
    print("Data inserted from console.")

# Обновление данных в таблице
def update_data(column_name, old_value, new_value):
    valid_columns = ["name", "surname", "phone"]
    if column_name not in valid_columns:
        print("Invalid column name.")
        return

    cur.execute(f"UPDATE phonebook SET {column_name} = %s WHERE {column_name} = %s", (new_value, old_value))
    conn.commit()
    print(f"Updated {column_name}: {old_value} -> {new_value}")

# Запрос данных с фильтром
def query_data(filter_column, filter_value):
    valid_columns = ["id", "name", "surname", "phone"]
    if filter_column not in valid_columns:
        print("Invalid filter column.")
        return
    
    cur.execute(f"SELECT * FROM phonebook WHERE {filter_column} = %s", (filter_value,))
    rows = cur.fetchall()
    if rows:
        print("Results found:")
        print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
    else:
        print("No records found.")

# Удаление данных по фильтру
def delete_data(filter_column, filter_value):
    valid_columns = ["name", "surname", "phone"]
    if filter_column not in valid_columns:
        print("Invalid column name.")
        return

    cur.execute(f"DELETE FROM phonebook WHERE {filter_column} = %s", (filter_value,))
    conn.commit()
    print(f"Deleted records where {filter_column} = {filter_value}")

# Основной цикл с выбором команд
check = True
command = ''
temp = ''
back = False

while check:
    if not back:
        print("""
        List of the commands:
        1. Type "i" or "I" to INSERT data into the table.
        2. Type "u" or "U" to UPDATE data in the table.
        3. Type "q" or "Q" to QUERY data from the table.
        4. Type "d" or "D" to DELETE data from the table.
        5. Type "f" or "F" to close the program.
        6. Type "s" or "S" to SEE the values in the table.
        """)
        command = str(input())

        # Вставка данных
        if command == "i" or command == "I":
            print('Type "csv" to upload from CSV or "con" to enter from console: ')
            command = str(input())
            if command == "con":
                insert_data_from_console()
            elif command == "csv":
                filepath = input("Enter the file path: ")
                insert_data_from_csv(filepath)
            back = True

        # Обновление данных
        if command == "u" or command == "U":
            temp = input('Type the column name to update (name, surname, phone): ')
            old_value = input(f'Enter current {temp}: ')
            new_value = input(f'Enter new {temp}: ')
            update_data(temp, old_value, new_value)
            back = True

        # Запрос данных
        if command == "q" or command == "Q":
            temp = input("Type the column name for filter (id, name, surname, phone): ")
            filter_value = input(f"Enter value for {temp}: ")
            query_data(temp, filter_value)
            back = True

        # Удаление данных
        if command == "d" or command == "D":
            temp = input("Type the column name to delete (name, surname, phone): ")
            filter_value = input(f"Enter {temp} to delete: ")
            delete_data(temp, filter_value)
            back = True

        # Просмотр всех данных
        if command == "s" or command == "S":
            cur.execute("SELECT * FROM phonebook;")
            rows = cur.fetchall()
            print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))
            back = True

        # Завершение работы
        if command == "f" or command == "F":
            check = False

# Закрытие соединения с базой данных
conn.commit()
cur.close()
conn.close()
