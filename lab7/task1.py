import pygame
import datetime

pygame.init()

a = pygame.display.set_mode((1000,650))
pygame.display.set_caption("Second")

b = pygame.image.load(r"C:\Users\gala\Desktop\My_subjects\pp2\labs\lab7\clock.png")
b = pygame.transform.scale(b,(1000, 650))

h = pygame.image.load(r"C:\Users\gala\Desktop\My_subjects\pp2\labs\lab7\rightarm.png")
h = pygame.transform.scale(h,(1000,700))

c = pygame.image.load(r"C:\Users\gala\Desktop\My_subjects\pp2\labs\lab7\leftarm.png")
c = pygame.transform.scale(c,(40,640))

run = True
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
            pygame.quit()
    a.blit(b,(0,0))

    x=datetime.datetime.now().hour%12
    e = c.get_rect(center=(490,320))
    f = pygame.transform.rotate(c,x*(-30))
    g = f.get_rect(center=e.center)
    a.blit(f,g)

    x=datetime.datetime.now().minute
    e = h.get_rect(center=(505,340))
    f = pygame.transform.rotate(h,x*(-6)+55)
    g = f.get_rect(center=e.center)
    a.blit(f,g)

    pygame.display.update()

        
    