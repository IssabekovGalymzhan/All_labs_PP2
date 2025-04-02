import pygame

pygame.init()
pygame.mixer.init()

a = pygame.display.set_mode((300,300))
pygame.display.set_caption("sound")

e=[pygame.mixer.Sound(r"C:\Users\gala\Desktop\My_subjects\pp2\labs\lab7\meow2.wav"), pygame.mixer.Sound(r"C:\Users\gala\Desktop\My_subjects\pp2\labs\lab7\mario_start.wav"), pygame.mixer.Sound(r"C:\Users\gala\Desktop\My_subjects\pp2\labs\lab7\mario_smert.wav")]
j=0

run = True
while run:
    u = pygame.event.wait()
    if u.type == pygame.QUIT:
        run = False
        pygame.quit()
    
    elif u.type == pygame.KEYDOWN:
        if u.key == pygame.K_q:
            j-=1
            if j<0:
                j=2
        elif u.key == pygame.K_w:
            j+=1
            if j>2:
                j=0
        elif u.key == pygame.K_SPACE:
            e[j].play()    
        elif u.key == pygame.K_TAB:
            e[j].stop()

    pygame.display.update()