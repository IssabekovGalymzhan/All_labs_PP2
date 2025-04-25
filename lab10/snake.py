import pygame
import sys
import random
import time
from db import save_user_game, get_user_game
import sys

# Получаем user_id из аргументов
user_id = int(sys.argv[1])

# --- Настройки уровней ---
levels = {
    1: {'speed': 10, 'walls': []},
    2: {'speed': 15, 'walls': [(100, 100), (120, 100), (140, 100)]},
    3: {'speed': 20, 'walls': [(200, 200), (220, 200), (240, 200), (260, 200)]}
}

# --- Настройки окна ---
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# --- Цвета ---
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY  = (100, 100, 100)

# --- Функция для отображения текста ---
def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")
clock = pygame.time.Clock()

# --- Восстановление состояния пользователя ---
loaded = get_user_game(user_id)
if loaded:
    score, level, saved_state = loaded
    if saved_state:
        snake = eval(saved_state)  # преобразуем строку обратно в список
    else:
        snake = [(100, 100)]
else:
    score = 0
    level = 1
    snake = [(100, 100)]

direction = (BLOCK_SIZE, 0)
food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
        random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

paused = False

# --- Основной цикл ---
running = True
while running:
    screen.fill(BLACK)

    # Рисуем стены
    for wall in levels[level]['walls']:
        pygame.draw.rect(screen, GRAY, (*wall, BLOCK_SIZE, BLOCK_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, BLOCK_SIZE):
                direction = (0, -BLOCK_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -BLOCK_SIZE):
                direction = (0, BLOCK_SIZE)
            elif event.key == pygame.K_LEFT and direction != (BLOCK_SIZE, 0):
                direction = (-BLOCK_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-BLOCK_SIZE, 0):
                direction = (BLOCK_SIZE, 0)
            elif event.key == pygame.K_p:
                # Сохраняем игру и выходим
                save_user_game(user_id, score, level, str(snake))
                print("Игра сохранена.")
                paused = True

    if paused:
        draw_text(screen, "Игра на паузе. Нажмите любую клавишу для выхода.", 20, 50, HEIGHT // 2, RED)
        pygame.display.flip()
        time.sleep(2)
        break

    # Движение змейки
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Проверка на столкновение со стенами или собой
    if (
        new_head in snake or
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in levels[level]['walls']
    ):
        draw_text(screen, "GAME OVER", 40, WIDTH // 3, HEIGHT // 2, RED)
        pygame.display.flip()
        time.sleep(2)
        save_user_game(user_id, 0, 1, None)
        break

    snake.insert(0, new_head)

    # Поел или нет
    if new_head == food:
        score += 1
        # Переход на следующий уровень
        if score % 5 == 0 and level < max(levels.keys()):
            level += 1
        food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
    else:
        snake.pop()

    # Отрисовка змеи и еды
    for part in snake:
        pygame.draw.rect(screen, GREEN, (*part, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))

    draw_text(screen, f"Уровень: {level}  Очки: {score}", 20, 10, 10)

    pygame.display.flip()
    clock.tick(levels[level]['speed'])

pygame.quit()
