import pygame 
import random
import math
import time
from random import randint
from pygame import mixer
# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Dino Run")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Import Background
background = pygame.image.load('night-background.png')

# Player
playerImage = pygame.image.load('dinosaur.png')
playerX = 100
playerY = 430
player_state = "ready"
playerY_change = -80

# Moon
moonImage = pygame.image.load('moon.png')
moonX = 600
moonY = 80

# Clouds
cloudImage = []
cloudX = []
cloudY = []
cloudX_change = []

cloud1 = pygame.image.load('cloud1.png')
cloud2 = pygame.image.load('cloud2.png')
for i in range(3):
    cloudImage.append(cloud1)
    cloudImage.append(cloud2)
    cloudX.append(randint(0,735))
    cloudX.append(randint(0,735))
    cloudY.append(randint(0,150))
    cloudY.append(randint(0,150))
num_of_clouds = 6
for i in range(num_of_clouds):
    cloudX_change.append(-1*random.uniform(0.0,0.9))

# Cactus
enemyImage= []
enemyX = []
enemyY= 430
enemyX_change = -4
enemyY_change = 0
enemy1 = pygame.image.load('cactus1.png')
enemy2 = pygame.image.load('cactus2.png')
enemy3 = pygame.image.load('cactus3.png')
num_of_enemies = 3
for i in range(num_of_enemies//3):
    enemyImage.append(enemy1)
    enemyImage.append(enemy2)
    enemyImage.append(enemy3)
for i in range(num_of_enemies//3):
    enemyX.append(randint(800,900))
    enemyX.append(randint(1100,1200))
    enemyX.append(randint(1500,1600))

# Bird
bird = pygame.image.load('bird.png')
num_of_birds = 3
birdImage = []
birdX = []
birdY = 375

birdX_change = -4
birdY_change = 0
for i in range(num_of_birds//3):
    for j in range(num_of_birds):
        birdImage.append(bird)
    birdX.append(randint(2200,3000))
    birdX.append(randint(4000,4050))
    birdX.append(randint(1750,1850))

# Score
score = 0
score_change = 0.01
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# High Score
high_score = open("highscore.txt","r")
high = high_score.read()
high = int(high)
high_score.close()
high_font = pygame.font.Font('freesansbold.ttf',16)
highX  = 10
highY = 50

# Game over text
over_font = pygame.font.Font('SEASRN__.ttf',64)
resume_font = pygame.font.Font('freesansbold.ttf',20)

# Background sound
mixer.init() 
#mixer.music.set_volume(0.7) 
mixer.music.load('song.mp3')
mixer.music.play(-1) # If we don't give -1 as argument then music is played only once
					# mixer.music is for long time but mixer.sound is for  short time

def player(x,y):
    screen.blit(playerImage,(x,y))

def moon():
    screen.blit(moonImage, (moonX,moonY))

def cloud(i):
    screen.blit(cloudImage[i], (cloudX[i], cloudY[i]))

def enemy(i):
    screen.blit(enemyImage[i], (enemyX[i],enemyY))

def  bird(i):
    screen.blit(birdImage[i], (birdX[i], birdY))

def isCollision(a, b, c, d):
    distance = math.sqrt(math.pow(a-c, 2)+math.pow(b-d,2))
    if distance <= 1 or distance-32 <=1:
        return True
    else:
        return False 

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,0,0))
    screen.blit(over_text, (200,250))
    author_text = resume_font.render("Author : Saran", True, (0,100,255))
    screen.blit(author_text, (310,500))

def restart_text():
    restart_text = resume_font.render("Press 'R' to restart", True, (0,100,255))
    screen.blit(restart_text, (300,500))

def show_pause_text():
    pause_text = resume_font.render("Press 'P' to pause", True, (0,100,255))
    screen.blit(pause_text, (600,30))

def pause_text():
    pause_text = over_font.render("PAUSED", True, (0,255,0))
    screen.blit(pause_text, (270,250))
    resume_text = resume_font.render("Press 'P' to resume", True, (0,100,255))
    screen.blit(resume_text, (290,500))

def show_score(x,y,s):
	score = font.render("Score : "+str(int(s)), True, (255,255,255))
	screen.blit(score, (x,y))

def show_high_score(x,y):
	h_score = high_font.render("High Score : "+ str(high), True, (255,255,255))
	screen.blit(h_score, (x,y))

def roar():
    dino = mixer.Sound('roar.wav')
    dino.play()

def paused():
    pause = True
    while pause:
        screen.fill((0,0,0))
        pause_text()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    time.sleep(0.1)
                    pause = False
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

# Game Loop
running = True
k = False
while running:
    screen.fill((0,0,0))
    # Background image
    screen.blit(background,(0,0))
    z=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score >= high:
                f = open("highscore.txt","w")
                f.write(str(int(score)))
                f.close()
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused()
            if player_state == "ready":
                if event.key == pygame.K_SPACE:
                    jump_sound = mixer.Sound('jump.wav')
                    jump_sound.play()
                    playerY += playerY_change
                    player_state = "jump"
                    count = 0
            else:
                playerY -= playerY_change
    
        if event.type == pygame.KEYUP:
            if player_state == "jump":
                count  = 0
                if event.key == pygame.K_SPACE:
                    playerY += -1*playerY_change   
                    player_state = "ready"
    
    # Cloud Boundary
    for i in range(num_of_clouds):
        cloudX[i] += cloudX_change[i]
        if cloudX[i]<=0:
            cloudX[i] = randint(0,735)
            cloudY[i] = randint(0,150)
            cloudX_change[i] = (-1*random.uniform(0.0,0.9))
        cloud(i)

    # Enemy Boundary
    for i in range(num_of_enemies):
        enemy(i)
        if isCollision(playerX,playerY,enemyX[i],enemyY) or k:
            mixer.music.stop()
            if k==False:
                roar()
            z=0
            for i in range(num_of_enemies):
                enemyX_change = 0
                enemyX[i] = 90000
            screen.fill((0,0,0))
            moonX = -100
            moonY = -100
            playerX = -100
            playerY = -100
            game_over_text()
            k = True
            break
        else:
            score += score_change
            high = int(max(high,score))
            
        enemyX[i] += enemyX_change
        if enemyX[i] <= 0:
            enemyX[i] = randint(1250, 1300)

    # Bird boundary
    for i in range(num_of_birds):
        bird(i)
        if isCollision(playerX,playerY,birdX[i],birdY) or k:
            mixer.music.stop()
            if k==False:
                roar()
            for i in range(num_of_birds):
                birdX_change = 0
                birdX[i] = 90000
            screen.fill((0,0,0))
            moonX = -100
            moonY = -100
            playerX = -100
            playerY = -100
            game_over_text()
            k = True
            break
        else:
            score += 0.01
            high = int(max(high,score))

        birdX[i] += birdX_change
        if birdX[i] <= 0:
            birdX[i] = randint(3000, 3050)
        for j in range(num_of_enemies):
            if abs(birdX[i] - enemyX[j]) <= 105 or abs(birdX[i] - enemyX[j]-32)<= 105 or abs(birdX[i] +32 - enemyX[j])<= 105:
                birdX[i] += 60
   
    player(playerX,playerY)
    show_score(textX,textY,score)
    show_high_score(highX, highY)
    show_pause_text()
    moon()
    pygame.display.update()