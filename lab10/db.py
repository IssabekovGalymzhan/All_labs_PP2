import psycopg2

#подключаюсь к базе данных
def connect():
    return psycopg2.connect(
        dbname="snake_game",
        user="postgres",
        password="Pg_sql_2025_pp2",
        host="localhost",
        port="5432"
    )

#создание таблиц user, user_score
def create_tables():
    conn=connect()
    cur=conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            score INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            saved_state TEXT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

# Получить ID пользователя или создать нового, если не существует
def get_or_create_user(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        user_id = result[0]
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return user_id

# Получить сохранённую игру (счёт, уровень, состояние)
def get_user_game(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT score, level, saved_state FROM user_score WHERE user_id = %s", (user_id,))
    data = cur.fetchone()

    cur.close()
    conn.close()
    return data

# Сохраняем игру (счёт, уровень, состояние)
def save_user_game(user_id, score, level, saved_state):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM user_score WHERE user_id = %s", (user_id,))
    if cur.fetchone():
        cur.execute("""
            UPDATE user_score
            SET score = %s, level = %s, saved_state = %s
            WHERE user_id = %s
        """, (score, level, saved_state, user_id))
    else:
        cur.execute("""
            INSERT INTO user_score (user_id, score, level, saved_state)
            VALUES (%s, %s, %s, %s)
        """, (user_id, score, level, saved_state))

    conn.commit()
    cur.close()
    conn.close()