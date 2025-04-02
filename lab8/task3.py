import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    x = 0
    y = 0
    mode = 'blue'
    points = []
    shape = 1 # Shape of circle is 1, shape of rectangle is 0
    erase_mode = False # 
        
            
    
    while True:
        
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        rect_held = pressed[pygame.K_1] # Change a shape to rectangle
        circle_held = pressed[pygame.K_2] # Change a shape to circle
        
        for event in pygame.event.get():
            
            # determin if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
                # determine if a letter key was pressed
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_y:
                    mode = 'yellow'
                elif event.key == pygame.K_c:
                    mode = 'cyan'
                elif event.key == pygame.K_p:
                    mode = 'pink'

                # Add erase mode
                if event.key == pygame.K_3:
                    erase_mode = True

                # determine if shape was changed
                if event.key == pygame.K_1:
                    shape = 1
                elif event.key == pygame.K_2:
                    shape = 0
                
                
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click grows radius
                    radius = min(200, radius + 1)
                elif event.button == 3: # right click shrinks radius
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEMOTION:
                # if mouse moved, add point to list

                position = event.pos
                points = points + [position]
                points = points[-256:]
                
        screen.fill((0, 0, 0))

        # draw all points
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode, shape)
            i += 1

        if erase_mode: # Add condition for erase mode
            screen.fill((0,0,0)) # Fill the display with black color
            points = [] # Update the list of position of mouse(delete all positions of colors)
            erase_mode = False # Return the erase mode to false
        pygame.display.update()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode, shape):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    elif color_mode == 'yellow': # Add 3 more colors: yellow, cyan and pink
        color = (c2, c2, c1)
    elif color_mode == 'cyan':
        color = (c1, c2, c2)
    elif color_mode == 'pink':
        color = (c2, c1, c2)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        if shape:
            pygame.draw.circle(screen, color, (x, y), width)
        else:
            pygame.draw.rect(screen, color, (x,y,width,width))

main()