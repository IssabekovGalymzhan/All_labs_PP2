from db import create_tables, get_or_create_user, get_user_game
import subprocess  # Запуск snake.py как отдельного процесса

# Создаём таблицы (если ещё не созданы)
create_tables()

# Спрашиваем имя игрока
username = input("Введите ваш username: ")
user_id = get_or_create_user(username)

# Пробуем загрузить прогресс
data = get_user_game(user_id)
if data:
    score, level, _ = data
    print(f"Добро пожаловать обратно, {username}!")
    print(f"Текущий уровень: {level}, счёт: {score}")
else:
    print(f"Новый игрок {username} создан.")

# Запускаем игру и передаём user_id как аргумент
subprocess.run(["python", "snake.py", str(user_id)])