import pygame
import random
import time
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="TEMA2007",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_scores (
    username TEXT REFERENCES users(username),
    score INTEGER,
    level INTEGER
)
''')

conn.commit()

# Ask for username and check if they exist in the database
username = input("Enter your username: ")

cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
user = cursor.fetchone()

if not user:
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    conn.commit()
    score = 0
    level = 1
    print(f"New user created: {username}. Starting at level {level}")
else:
    cursor.execute("SELECT score, level FROM user_scores WHERE username = %s ORDER BY score DESC LIMIT 1", (username,))
    data = cursor.fetchone()
    if data:
        score, level = data
        print(f"Welcome back, {username}! Resuming from level {level}, score {score}")
    else:
        score = 0
        level = 1
        print(f"Welcome back, {username}! No previous score found.")

# Initialize Pygame
pygame.init()

# Display settings
width, height = 800, 600
black, white, gray, green, red, blue = (0, 0, 0), (255, 255, 255), (128, 128, 128), (0, 255, 0), (255, 0, 0), (0, 0, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with Levels and Timed Food")

fruit_eaten, done = False, False
speed = max(50, 200 - (level * 20))

# Snake
head_square = [100, 100]
squares = [[30, 100], [40, 100], [50, 100], [60, 100], [70, 100], [80, 100], [90, 100], [100, 100]]
direction, next_dir = "right", "right"

# Food
food_types = [
    {"color": green, "points": 10},
    {"color": red, "points": 20},
    {"color": blue, "points": 30}
]

# Walls for levels
walls = {
    2: [[200, 200], [210, 200], [220, 200], [230, 200]],
    3: [[400, 300], [410, 300], [420, 300], [430, 300]],
}

def check_wall_collision(head):
    if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
        return True
    if level in walls:
        if head in walls[level]:
            return True
    return False

def generate_food():
    while True:
        fr_x = random.randrange(1, width // 10) * 10
        fr_y = random.randrange(1, height // 10) * 10
        food = random.choice(food_types)
        if [fr_x, fr_y] not in squares and (level not in walls or [fr_x, fr_y] not in walls[level]):
            return {"coord": [fr_x, fr_y], "color": food["color"], "points": food["points"], "spawn_time": time.time()}

fruit = generate_food()
food_timer = 10  # 10 sec

def game_over():
    global done
    cursor.execute(
        "INSERT INTO user_scores (username, score, level) VALUES (%s, %s, %s)",
        (username, score, level)
    )
    conn.commit()

    font = pygame.font.SysFont("times new roman", 45)
    text = font.render(f"Game Over! Your score: {score}", True, gray)
    screen.fill(black)
    screen.blit(text, text.get_rect(center=(width // 2, height // 2)))
    pygame.display.update()
    pygame.time.delay(1000)  # Reduced delay
    pygame.quit()
    cursor.close()
    conn.close()
    exit()

def display_high_scores():
    # Retrieve top 5 high scores from the database
    cursor.execute("""
    SELECT username, score, level FROM user_scores
    ORDER BY score DESC
    LIMIT 5
    """)
    high_scores = cursor.fetchall()

    font = pygame.font.SysFont("times new roman", 30)
    screen.fill(black)
    title = font.render("Top 5 High Scores", True, white)
    screen.blit(title, (width // 2 - title.get_width() // 2, 50))

    for i, (user, score, level) in enumerate(high_scores):
        score_text = font.render(f"{i + 1}. {user}: Score: {score} - Level: {level}", True, white)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 100 + i * 40))

    pygame.display.update()
    pygame.time.delay(3000)  # Show high scores for 3 seconds

# Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and direction != "up":
                next_dir = "down"
            if event.key == pygame.K_UP and direction != "down":
                next_dir = "up"
            if event.key == pygame.K_LEFT and direction != "right":
                next_dir = "left"
            if event.key == pygame.K_RIGHT and direction != "left":
                next_dir = "right"
            if event.key == pygame.K_p:
                # Pause and save the game state
                print("Game paused and saved. Press P to resume.")
                cursor.execute(
                    "INSERT INTO user_scores (username, score, level) VALUES (%s, %s, %s)",
                    (username, score, level)
                )
                conn.commit()
                paused = True
                while paused:
                    for e in pygame.event.get():
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                            paused = False
            if event.key == pygame.K_h:
                # Display high scores when 'H' is pressed
                display_high_scores()

    # Check for self-collision
    for square in squares[:-1]:
        if head_square == square:
            game_over()
    if check_wall_collision(head_square):
        game_over()

    direction = next_dir

    # Movement
    if direction == "right":
        head_square[0] += 10
    elif direction == "left":
        head_square[0] -= 10
    elif direction == "up":
        head_square[1] -= 10
    elif direction == "down":
        head_square[1] += 10

    new_square = [head_square[0], head_square[1]]
    squares.append(new_square)

    # Food eaten
    if head_square == fruit["coord"]:
        fruit_eaten = True
        score += fruit["points"]
    else:
        squares.pop(0)

    # Check food timer
    if time.time() - fruit["spawn_time"] > food_timer:
        fruit_eaten = True

    if fruit_eaten:
        fruit = generate_food()
        fruit_eaten = False

    # Update level and speed
    level = score // 30 + 1
    speed = max(50, 200 - (level * 20))

    # Render
    screen.fill(black)
    font = pygame.font.SysFont("times new roman", 20)
    score_surface = font.render(f"User: {username}  Score: {score}  Level: {level}", True, gray)
    screen.blit(score_surface, (20, 20))

    # Draw walls
    if level in walls:
        for wall in walls[level]:
            pygame.draw.rect(screen, gray, pygame.Rect(wall[0], wall[1], 10, 10))

    # Draw food
    pygame.draw.circle(screen, fruit["color"], (fruit["coord"][0] + 5, fruit["coord"][1] + 5), 5)

    # Draw snake
    for el in squares:
        pygame.draw.rect(screen, white, pygame.Rect(el[0], el[1], 10, 10))

    pygame.display.flip()

    pygame.time.delay(speed)

cursor.close()
conn.close()
pygame.quit()
