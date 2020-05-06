# Fedya Cheltsov, 05.05.2020, Snake Game with Pygame
import pygame
import random
from collections import Counter

pygame.init()
pygame.mixer.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
cyan = (0,255,255)

block=20
width=40
height=30
screenWidth = block*width
screenHeight = block*height

screen=pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Game')

clock = pygame.time.Clock()

def uniqueList(list):
    uniqueList=[]
    for element in list:
        if element not in uniqueList:
            uniqueList.append(element)
    return len(uniqueList)

def countDistinct(arr):
    return len(Counter(arr).keys())

def Message(msg,colour,size,x,y):
    fontStyle = pygame.font.SysFont(None, size)
    message = fontStyle.render(msg, True, colour)
    screen.blit(message, [x,y])

def printBody(count,array):
    for x in range(-count+1,0):
        pygame.draw.rect(screen, red, [array[-x][0],array[-x][1],block,block])

def updateBody(x,y,matrix,factor):
    if factor==True:
        del matrix[-1]
        matrix.insert(0,[x,y])

def paused():
    
    pause=True
    while pause==True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.Channel(0).set_volume(0.5)
                    pause=False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def spawnFruit(x,y):
    pygame.draw.rect(screen, red, [x, y, block, block])

gridArray=[]
for x in range(width):
    for y in range(height):
        gridArray.append([x*block,y*block])

highscore=0

bg = pygame.mixer.Sound('knightmare.wav')
pop = pygame.mixer.Sound('pop.wav')
pop2 = pygame.mixer.Sound('pop_heavy.wav')

def GAME_LOOP():
    pygame.mixer.Channel(0).play(bg,-1)
    pygame.mixer.Channel(0).set_volume(0.5)
    fruitColour=green
    lastCommand=0
    score=0
    length=1
    gameOver=False
    gameClosed=False
    fruitPresent=False
    active=True
    x = int(screenWidth/2)
    y = int(screenHeight/2)
    
    x_change = 0
    y_change = 0
    
    snakeBody=[[] for x in range(width*height)]
    updateBody(x,y,snakeBody,active)
    
    active=False
    while gameOver==False:
        
        while gameClosed==True:
            pygame.mixer.Channel(0).set_volume(0.1)
            global highscore
            if score>highscore:
                highscore=score
            screen.fill(white)
            highscoreStr="Highscore: "+str(highscore)
            Message("You Lost! Press Q to quit or R to play again!",red,25,screenWidth*0.05,screenHeight*0.5)
            Message(highscoreStr,red,25,screenWidth*0.05,screenHeight*0.4)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = True
                        gameClosed = False
                    if event.key == pygame.K_r:
                        pygame.mixer.Channel(0).set_volume(0.5)
                        GAME_LOOP()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        pressed=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:

                
                
                if event.key == pygame.K_LEFT:
                    if pressed == False:
                        if lastCommand != pygame.K_RIGHT and length > 1:
                            x_change = -block
                            y_change = 0
                            lastCommand=pygame.K_LEFT
                            pressed=True
                        elif length==1:
                            x_change = -block
                            y_change = 0
                            lastCommand=pygame.K_LEFT
                            pressed=True
                if event.key == pygame.K_RIGHT:
                    if pressed == False:
                        if lastCommand != pygame.K_LEFT and length > 1:
                            x_change = block
                            y_change = 0
                            lastCommand=pygame.K_RIGHT
                            pressed=True
                        elif length==1:
                            x_change = block
                            y_change = 0
                            lastCommand=pygame.K_RIGHT
                            pressed=True
                if event.key == pygame.K_DOWN:
                    if pressed == False:
                        if lastCommand != pygame.K_UP and length > 1:
                            x_change = 0
                            y_change = block
                            lastCommand=pygame.K_DOWN
                            pressed=True
                        elif length==1:
                            x_change = 0
                            y_change = block
                        lastCommand=pygame.K_DOWN
                        pressed=True
                if event.key == pygame.K_UP:
                    if pressed == False:
                        if lastCommand != pygame.K_DOWN and length > 1:
                            x_change = 0
                            y_change = -block
                            lastCommand=pygame.K_UP
                            pressed=True
                        elif length==1:
                            x_change = 0
                            y_change = -block
                            lastCommand=pygame.K_UP
                            pressed=True                
                
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_p:
                    pygame.mixer.Channel(0).set_volume(0.1)
                    paused()
            active=True
        x += x_change
        y += y_change
        screen.fill(black)

        updateBody(x,y,snakeBody,active)

        if snakeBody[0] in snakeBody[1:length]:
            gameClosed=True

        if fruitPresent==False:
            fruitArray=[x for x in gridArray if x not in snakeBody[0:score+1]]
            position=random.randint(0,len(fruitArray)-1)
            fruitWidth=fruitArray[position][0]
            fruitHeight=fruitArray[position][1]
            fruitPresent=True

        if x==fruitWidth and y==fruitHeight:
            
            if fruitColour==cyan:
                pygame.mixer.Channel(1).play(pop2)
                length+=10
                score+=10
            else:
                pygame.mixer.Channel(1).play(pop)
                length+=2
                score+=2
            if uniqueList(snakeBody)>=15:
                randomFactor=random.randint(0,7)
                if randomFactor==7:
                    fruitColour=cyan
                else:
                    fruitColour=green

            fruitPresent=False
            
        scoreStr="SCORE: "+str(score)
        highscoreStr="HIGHSCORE: "+str(highscore)
        Message(highscoreStr, white,20,screenWidth-100,10)
        Message(scoreStr,white,20,10,10)
        Message("Press P to pause/unpause or Q to quit",white,20,10,screenHeight-20)

        pygame.draw.rect(screen, fruitColour, [fruitWidth, fruitHeight, block, block])
        pygame.draw.rect(screen, red, [x, y, block, block])

        if length>1:
            printBody(length,snakeBody)

        pygame.display.update()
    
        clock.tick(10)
        
        if x >= screenWidth or x < 0 or y >= screenHeight or y < 0:
            gameClosed = True

    pygame.quit()
    exit()
    
GAME_LOOP()