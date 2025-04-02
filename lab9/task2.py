import pygame
import time
import random

snake_speed = 10
timer = 0

# Window size
window_x = 1000
window_y = 500

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Custom Caption')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
# fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                  random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score, level and food that we have eaten
score = 0; level = 1; food = 0

# We will have 2 types of food>>> 0 - regular food, 1 - special food. Fruit type also points at index of lists fruit_value and score_value
fruit_type = 0
fruit_value = [1,3] # values of fruits shows how fast our speed will increase, and how many points we will get to score
score_value = [10,30]


# displaying Score function
#show_score(1, blue, 'times new roman', 35)
def show_score_and_level(choice, color, font, size):
  
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)
    
    level_font = pygame.font.SysFont(font, size) # Add font and size for level-text

    # create the display surface object 
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    level_surface = level_font.render('Level : ' + str(level), True, color) # Add some surface for level-text
    
    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()

    level_rect = level_surface.get_rect(topright=(995,0)) # The coordinates of level-text
    
    # displaying text
    game_window.blit(score_surface, score_rect)
    game_window.blit(level_surface, level_rect) # Add level text on screen



# game over function
def game_over():
  
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # creating a text surface on which text 
    # will be drawn
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score) + "    Your level is : " + str(level), True, red)
    
    # create a rectangular object for the text 
    # surface object
    game_over_rect = game_over_surface.get_rect()
    
    # setting position of the text
    game_over_rect.center = (window_x/2, window_y/4)
    # game_over_rect.centerx = 500
    
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.update()
    
    # after 2 seconds we will quit the program
    time.sleep(2)
    
    # deactivating pygame library
    pygame.quit()
    
    # quit the program
    quit()

# Main Function
while True:
    if fruit_position[0]>=475 and fruit_position[0]<=525 and  fruit_position[1]>=200: # If fruit position is inside of border, then update fruit position to new one
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]
        
    
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
    

    # If two keys pressed simultaneously
    # we don't want snake to move into two 
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    c = pygame.Surface((1,1))
    d = c.get_rect(center=(snake_position[0], snake_position[1])) # Make a rect object on position of the head of snake 

    a = pygame.Surface((50,300)) # Add surface of border
    a.fill((120,0,0))
    b = a.get_rect(midbottom=(500,500)) # Add rect object as a border

    if b.colliderect(d): # To check if border collides the position of snake`s head
        game_over()


    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += score_value[fruit_type]
        food += fruit_value[fruit_type]
        fruit_spawn = False
    else:
        snake_body.pop()

    if food>=3: # If snake eats food 3 times, speed will increase and we will go to the next level
        snake_speed+=10
        food-=3 # Update the counter of food
        level+=1
        
    if not fruit_spawn:
        fruit_type = random.randrange(0,2)
        if fruit_type:
            timer=0
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]
        
    fruit_spawn = True
    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    if not fruit_type:
        pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))
    else:
        pygame.draw.rect(game_window, (255, 140, 0), pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score continuously
    show_score_and_level(1, blue, 'times new roman', 35)

    game_window.blit(a,b)

    timer+=1 # Varable "timer" increases every iteration, but we have "snake_speed" numbers of iteration in one second. It means that we can multiply both sides with "snake_speed"
    if timer>=10*snake_speed and fruit_type: # If both conditions are true, we will update our timer and place on screen regular fruit.
        timer=0
        fruit_type = 0
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]


    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
