import pygame

pygame.init()
t = pygame.time.Clock()

a = pygame.display.set_mode((500,500))
pygame.display.set_caption("ball")

x,y=250,250

pygame.draw.circle(a, (200,0,0), (x,y), 25, 0)

run = True
while run:
    a.fill((255,255,255))
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
            pygame.quit()

    u = pygame.key.get_pressed()
    if u[pygame.K_w] and y-20>=25:
        y-=20
    elif u[pygame.K_d] and x+20<=475:
        x+=20
    elif u[pygame.K_a] and x-20>=25:
        x-=20
    elif u[pygame.K_s] and y+20<=475:
        y+=20

    pygame.draw.circle(a, (200,0,0), (x,y), 25, 0)
    pygame.display.update()
    t.tick(25)