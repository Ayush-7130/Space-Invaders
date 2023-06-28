import pygame
import random
import math
from pygame import mixer

# initialise pygame module
pygame.init()
pygame.display.set_caption('Space Invaders')

icon = pygame.image.load('images\\spaceship.png')
pygame.display.set_icon(icon)


# window screen formed
width=400
height=600
screen = pygame.display.set_mode((width,height))

# # Title and LOOP
# pygame.display.set_caption("First Game")
# icon = pygame.image.load("a.png")
# pygame.display.set_icon(icon)

# add player
playerimg = pygame.image.load("images\space-invaders.png")
playerX = (width - playerimg.get_height())/2
playerY = height - 100
U_playerX = 0
U_playerY = 0

# background
background=pygame.image.load("images\\background.png")
back_sound = mixer.Sound("sound\\background.wav")
back_sound.play(-1)

# start
startimg = pygame.image.load("images\\start_edited.png")

# gameover
gameoverimg = pygame.image.load("images\\gameover.png")

# enemy
enemyimg = []
enemyX = []
enemyY = []
U_enemyX = []
U_enemyY = []

num_of_enemies = 6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("images\\ghost.png"))
    enemyX.append((random.randint(0,width) - 32)/2)
    enemyY.append(random.randint(0,height/3))
    # U_enemyX.append(0.1)
    U_enemyX.append(1.4)
    U_enemyY.append(32)

# bullets
bulletimg = pygame.image.load("images\\bullet.png")
bullet_state = "ready"
bulletX = 0
bulletY = 0
U_bulletY = 3.5

# screen.fill((255,255,0))
# pygame.display.update()

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x,y))
    # pygame.

def iscollide(eX,eY,bX,bY):
    distance = math.sqrt(math.pow(eX - bX, 2) + (math.pow(eY - bY, 2)))
    if(distance < 27):
        return True
    return False

score = 0

def display_score(x,y,r,b,g,sz):
    font =pygame.font.Font('font\\Stop Bullying.otf',sz)
    score_1 = font.render("Score : "+str(score),True,(r,b,g))
    screen.blit(score_1,(x,y))

def isgameover(eX,eY,pX,pY):
    distance = math.sqrt(math.pow(eX - pX, 2) + (math.pow(eY - pY, 2)))
    if(distance < 27):
        return True
    return False

running = False
close = False
gameover = False

if __name__=="__main__":
    # game loop 

    while running == False and close == False:
        screen.fill((0,0,0)) 
        screen.blit(startimg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = True
            if event.type == pygame.QUIT:
                close = True
        pygame.display.update()

    while running == True and close == False:
        if gameover == False:
            #           (R,G,B)
            screen.fill((0,0,0))     
            screen.blit(background,(0,0))                   
            # background file is large  so we have to change the movement of enemy and space ship
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        # U_playerX = 0.1
                        U_playerX = 2

                    elif event.key == pygame.K_LEFT:
                        # U_playerX = -0.1
                        U_playerX = -2

                    elif event.key == pygame.K_UP:
                        # U_playerY = -0.1
                        U_playerY = -2

                    elif event.key == pygame.K_DOWN:
                        # U_playerY = 0.1
                        U_playerY = 2

                    elif event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bullet_shoot = mixer.Sound("sound\\laser.wav")
                            bullet_shoot.play()
                            bulletX = playerX + 16
                            bulletY = playerY + 10
                            bullet(bulletX,bulletY)

                    else:
                        U_playerX = 0
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        U_playerX = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        U_playerY = 0
                    
            playerX += U_playerX
            playerY += U_playerY

            if(playerX <=0):
                playerX = 0
            elif(playerX >= 336):
                playerX = 336

            if(playerY <= 2*height/3):
                    # pass
                playerY = 2*height/3
            elif(playerY >= height-64):
                playerY=height-64

            if bullet_state == "fire":
                bullet(bulletX,bulletY)
                bulletY -= U_bulletY

            if bulletY <= 0:
                bullet_state = "ready"
                
            for i in range(num_of_enemies):

                enemyX[i] += U_enemyX[i]
                if(enemyX[i] <= 0):
                    # U_enemyX[i] = 0.1
                    U_enemyX[i] = 1.4
                    enemyY[i] += U_enemyY[i]
                        
                elif(enemyX[i] >= 368):
                    # U_enemyX[i] = -0.1
                    U_enemyX[i] = -1.4
                    enemyY[i] += U_enemyY[i]
                
                collision = iscollide(enemyX[i],enemyY[i],bulletX,bulletY)

                if collision == True:
                    explosion_sound = mixer.Sound("sound\\explosion.wav")
                    explosion_sound.play()
                    bulletY = playerY
                    bullet_state = "ready"
                    score +=1\
                    # print(score)
                    enemyX[i] = (random.randint(33,width) - 32)/2
                    enemyY[i] = random.randint(5,height/3)
                enemy(enemyX[i],enemyY[i],i)
                display_score(10,10,255,255,255,12)
            
            for i in range(num_of_enemies):
                gameover = isgameover(enemyX[i],enemyY[i],playerX,playerY)
                if gameover == True:
                    break
                    
            player(playerX,playerY)
            pygame.display.update()

        if gameover == True:
            screen.fill((0,0,0)) 
            screen.blit(gameoverimg,(0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameover = False
                        score = 0
                        for i in range(num_of_enemies):
                            enemyX[i] = (random.randint(33,width) - 32)/2
                            enemyY[i] = random.randint(5,height/3)

            display_score(130,100,0,0,0,24)
            pygame.display.update()