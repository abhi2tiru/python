from sys import byteorder
import pygame
import os
pygame.font.init()
WIDTH , HEIGHT=900, 500
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
SPACE=pygame.transform.scale(pygame.image.load(os.path.join('ASSETS','space.png')),(WIDTH,HEIGHT))
YELLOW=(255,255,0)
FPS=60
v=5
bv=10
max=3
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("TWO PLAYER SHOOTOUT")
YELLOW_IMAGE=pygame.image.load(os.path.join('ASSETS','spaceship_yellow.png'))
RED_IMAGE=pygame.image.load(os.path.join('ASSETS','spaceship_red.png'))
border=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
Y_I=pygame.transform.rotate(pygame.transform.scale(YELLOW_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
R_I=pygame.transform.rotate(pygame.transform.scale(RED_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
def handle_collisions(yellow,red,yb,rb,h):
    for b in yb:
        b.x+=v
        if red.colliderect(b):
            yb.remove(b)
            h[1]-=1
            continue
        pygame.draw.rect(WIN,(255,0,255),b)
        if b.x>WIDTH:
            yb.remove(b)    
    for b in rb:
        b.x-=v
        if yellow.colliderect(b):
            rb.remove(b)
            h[0]-=1
            continue
        pygame.draw.rect(WIN,RED,b)
        if b.x<0:
            rb.remove(b)
def draw_window(yellow,red,yb,rb,h):
    WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN,BLACK,border)
    WIN.blit(Y_I,(yellow.x,yellow.y))
    WIN.blit(R_I,(red.x,red.y))
    handle_collisions(yellow,red,yb,rb,h)
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(h[1]), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(h[0]), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))            
    pygame.display.update()
def handle_movement(k_p,yellow,red):
    if k_p[pygame.K_a] and yellow.x-v>0:
            yellow.x-=v
    if k_p[pygame.K_d] and yellow.x+v+SPACESHIP_WIDTH<WIDTH//2-5:
        yellow.x+=v
    if k_p[pygame.K_w] and yellow.y-v>=0:
        yellow.y-=v    
    if k_p[pygame.K_s] and yellow.y+v+SPACESHIP_HEIGHT+15<HEIGHT:
        yellow.y+=v
    if k_p[pygame.K_UP] and red.y-v>=0:
        red.y-=v
    if k_p[pygame.K_DOWN] and red.y+v+SPACESHIP_WIDTH<HEIGHT:
        red.y+=v
    if k_p[pygame.K_LEFT] and red.x-v>=WIDTH//2+5:
        red.x-=v    
    if k_p[pygame.K_RIGHT] and red.x+v+SPACESHIP_WIDTH<=WIDTH+10:
        red.x+=v
def handle_winner(WIN,h):
    if h[0]==0:
            text="RED PLAYER WINS!"        
    if h[1]==0:
            text="YELLOW PLAYER WINS"
    if h[0]==0 or h[1]==0:
        WIN.blit(HEALTH_FONT.render(text, 1, WHITE), (WIDTH//4, 200))
        pygame.display.update()
        pygame.time.delay(5000)
        return True 
    else:
        return False    
def main():
    run=True
    text=""
    yellow=pygame.Rect(200,200,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red=pygame.Rect(700,200,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    rb,yb=[],[]
    yh,rh=5,5
    h=[5,5]
    while run:
        clock=pygame.time.Clock()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(yb)<max:
                    bullet=pygame.Rect(yellow.x+SPACESHIP_WIDTH,yellow.y+SPACESHIP_HEIGHT//2+5,10,2)
                    yb.append(bullet)
                if event.key==pygame.K_RCTRL and len(rb)<max:
                    bullet=pygame.Rect(red.x,red.y+SPACESHIP_HEIGHT//2+5,10,2)
                    rb.append(bullet)    
        k_p=pygame.key.get_pressed()
        handle_movement(k_p,yellow,red)
        if handle_winner(WIN,h):
            break
        draw_window(yellow,red,yb,rb,h)
    main()        
if __name__=="__main__":
    main()    