import os
import psycopg2
import csv

# подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="Galymzhan_8"
)
cur = conn.cursor()

# Создание таблицы
cur.execute('''
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        phone VARCHAR(20)
    )
''')
conn.commit()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute('INSERT INTO phonebook (name, phone) VALUES (%s, %s)', (name, phone))
    conn.commit()
    print("Inserted successfully.")

def insert_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cur.execute('INSERT INTO phonebook (name, phone) VALUES (%s, %s)', (row[0], row[1]))
    conn.commit()
    print("CSV data inserted successfully.")

def update_data():
    id = input("Enter id to update: ")
    new_name = input("Enter new name: ")
    new_phone = input("Enter new phone: ")
    cur.execute('UPDATE phonebook SET name = %s, phone = %s WHERE id = %s', (new_name, new_phone, id))
    conn.commit()
    print("Updated successfully.")

def query_data():
    choice = input("Filter by (1) Name, (2) Phone, (3) All: ")
    if choice == '1':
        name = input("Enter name to search: ")
        cur.execute('SELECT * FROM phonebook WHERE name ILIKE %s', ('%' + name + '%',))
    elif choice == '2':
        phone = input("Enter phone to search: ")
        cur.execute('SELECT * FROM phonebook WHERE phone ILIKE %s', ('%' + phone + '%',))
    else:
        cur.execute('SELECT * FROM phonebook')
    
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_data():
    choice = input("Delete by (1) Name or (2) Phone: ")
    if choice == '1':
        name = input("Enter name to delete: ")
        cur.execute('DELETE FROM phonebook WHERE name = %s', (name,))
    else:
        phone = input("Enter phone to delete: ")
        cur.execute('DELETE FROM phonebook WHERE phone = %s', (phone,))
    conn.commit()
    print("Deleted successfully.")

def main():
    while True:
        print("\n1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update data")
        print("4. Query data")
        print("5. Delete data")
        print("6. Exit")

        choice = input("Choose option: ")
        if choice == '1':
            insert_from_console()
        elif choice == '2':
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == '3':
            update_data()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_data()
        elif choice == '6':
            break
        else:
            print("Invalid option.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
