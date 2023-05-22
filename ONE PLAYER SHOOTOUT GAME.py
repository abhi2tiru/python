import pygame
import os
import random
pygame.font.init()
HEALTH=3
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40  # size of spaceship
ENEMY_WIDTH,ENEMY_HEIGHT=50,30
ENEMY=pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_red.png')),(ENEMY_WIDTH,ENEMY_HEIGHT))
SPACESHIP=pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_yellow.png')),(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),180)
WIDTH,HEIGHT=500,700                    # size of the game window
SPACE=pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT)),180)
SPACESHIP_SPEED=4                       #speed of spaceship 
ENEMY_SPEED=5                           # speed of enemy
BULLET_WIDTH,BULLET_HEIGHT=5,10         # size of bullets
MAX_BULLETS=3                           # maximum number of bullets that can appear on screen 
FPS=60                                  # frames per second
WHITE=(255,255,255)
BULLET_COLOR=(255,0,0)                  # color of bullets
BULLET_SPEED=7                          # speed of bullets
SCORE_PER_ENEMY=1
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))
def draw_window(spaceship,bullets,enemies,lives,score):
    WINDOW.blit(SPACE,(0,0))
    WINDOW.blit(SPACESHIP,(spaceship.x,spaceship.y))
    health_text = HEALTH_FONT.render(
        "HEALTH: " + str(lives[0]), 1, WHITE)
    score_text = HEALTH_FONT.render(
        "SCORE: " + str(score[0]), 1, WHITE)
    WINDOW.blit(health_text, (WIDTH - health_text.get_width() - 10, 10))
    WINDOW.blit(score_text, (10, 10))
    for bullet in bullets:
        pygame.draw.rect(WINDOW,BULLET_COLOR,bullet)
        bullet.y-=BULLET_SPEED
        if bullet.y<0:
            bullets.remove(bullet)
    for enemy in enemies:
        WINDOW.blit(ENEMY,(enemy.x,enemy.y))
        enemy.y+=ENEMY_SPEED
        if enemy.y>HEIGHT:
            enemies.remove(enemy)
            lives[0]-=1        
    pygame.display.update()
def handle_spaceship(keys,spaceship):
    if keys[pygame.K_LEFT] and spaceship.x-SPACESHIP_SPEED>=0:
        spaceship.x-=SPACESHIP_SPEED
    if keys[pygame.K_RIGHT] and spaceship.x+SPACESHIP_SPEED+SPACESHIP_WIDTH<=WIDTH:
        spaceship.x+=SPACESHIP_SPEED
def handle_event(event,spaceship,bullets):
    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_SPACE and len(bullets)<MAX_BULLETS:
            bullets.append(pygame.Rect(spaceship.x+SPACESHIP_WIDTH//2,HEIGHT-SPACESHIP_HEIGHT,BULLET_WIDTH,BULLET_HEIGHT))    
def handle_collisions(bullets,enemies,score):
    for bullet in bullets:
        man=True
        for enemy in enemies:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                score[0]+=SCORE_PER_ENEMY
                man=False
        if man==False:
            bullets.remove(bullet)
def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)            
def main():
    clock=pygame.time.Clock()
    spaceship=pygame.Rect(WIDTH//2-SPACESHIP_WIDTH//2,HEIGHT-SPACESHIP_HEIGHT,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    run=True
    count=0
    bullets,enemies,lives=[],[],[]
    lives.append(HEALTH)
    score=[0]
    while run:
        clock.tick(FPS) # TO SLOW THE GAME SPEED AND SET THE FPS
        count+=1
        if count%100==0:
            enemies.append(pygame.Rect(random.randint(0,WIDTH-ENEMY_WIDTH),0,ENEMY_WIDTH,ENEMY_HEIGHT))
        handle_collisions(bullets,enemies,score)    
        draw_window(spaceship,bullets,enemies,lives,score)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                print(lives[0],score[0])
                break
            handle_event(event,spaceship,bullets,) 
        key=pygame.key.get_pressed()
        handle_spaceship(key,spaceship)
        winner_text = ""
        if lives[0] <= 0:
            winner_text = "LOST"

        for enemy in enemies:
            if spaceship.colliderect(enemy):
                winner_text = "BOOM"       

        if winner_text != "":
            draw_winner(winner_text)
            break
if __name__=="__main__":
    main()    