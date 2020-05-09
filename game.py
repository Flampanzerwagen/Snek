# EPIC SNEK GAME
import pygame
import random

pygame.init()
pygame.mixer.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
red2 = (200,0,0)
green = (0,255,0)
cyan = (0,255,255)
pink = (255,0,144)
indigo = (75,0,130)
orange = (255,100,0)


block=20
width=25
height=25

screenWidth = block*width
screenHeight = block*height



snakeBody=[[] for x in range(width*height)]
length=1

screen=pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Game')

clock = pygame.time.Clock()

def uniqueList(list):
    uniqueList=[]
    for element in list:
        if element not in uniqueList:
            uniqueList.append(element)
    return len(uniqueList)

def Message(msg,colour,size,x,y):
    fontStyle = pygame.font.SysFont(None, size)
    message = fontStyle.render(msg, True, colour)
    screen.blit(message, [x,y])

def printBody(count,array):
    try:
        for x in range(-count+1,0):
            pygame.draw.rect(screen, red, [array[-x][0],array[-x][1],block,block])
    except:
        pass
        
def updateBody(x,y,matrix,factor):
    if factor==True:
        del matrix[-1]
        matrix.insert(0,[x,y])

def paused():
    Message("PAUSED", white,40,screenWidth*0.4,screenHeight*0.5)
    pygame.display.update()
    pause=True
    while pause==True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Channel(0).set_volume(0.5)
                    pause=False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

gridArray=[]
for x in range(width):
    for y in range(height):
        gridArray.append([x*block,y*block])

file = open("data/highscore.txt","r")
highscore=int(file.read())
file.close()

bg = pygame.mixer.Sound('data/knightmare.wav')
sound = pygame.mixer.Sound('data/sound.wav')

wallsSaved = True
godModeSaved = False

def GAME_LOOP():    
    pygame.mixer.Channel(0).play(bg,-1)
    pygame.mixer.Channel(0).set_volume(0.1)
    global godModeSaved
    global wallsSaved
    godMode=godModeSaved
    walls=wallsSaved
    difficultyChosen = False
    
    while difficultyChosen == False:
        screen.fill(white)
        Message("Choose difficulty: ",red,30,screenWidth*0.1,screenHeight*0.1)
        Message("Easy: '1'",red,25,screenWidth*0.05,screenHeight*0.2)
        Message("Medium: '2' ( Recommended )",red,25,screenWidth*0.05,screenHeight*0.3)
        Message("Hard: '3'",red,25,screenWidth*0.05,screenHeight*0.4)
        Message("Insane: '4'",red,25,screenWidth*0.05,screenHeight*0.5)
        Message("Press Q to quit",red,20,10,screenHeight-20)
        if walls == False:
            Message("Walls: '5' ( Disabled )",red,25,screenWidth*0.05,screenHeight*0.7)
        else:
            Message("Walls: '5' ( Enabled )",red,25,screenWidth*0.05,screenHeight*0.7)
        if godMode == False:
            Message("God mode ( Auto No Walls ): '6' ( Disabled )",red,25,screenWidth*0.05,screenHeight*0.8)
        else:
            Message("God mode ( Auto No Walls ): '6' ( Enabled )",red,25,screenWidth*0.05,screenHeight*0.8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()    
                elif event.key == pygame.K_1:
                    difficulty = 1
                    difficultyChosen = True
                elif event.key == pygame.K_2:
                    difficulty = 2
                    difficultyChosen = True
                elif event.key == pygame.K_3:
                    difficulty = 3
                    difficultyChosen = True
                elif event.key == pygame.K_4:
                    difficulty = 4
                    difficultyChosen = True
                elif event.key == pygame.K_5 and walls == True:
                    walls = False
                    wallsSaved=False
                elif event.key == pygame.K_5 and walls == False:
                    walls = True
                    wallsSaved=True
                elif event.key == pygame.K_6 and godMode == False:
                    godMode = True
                    godModeSaved = True
                elif event.key == pygame.K_6 and godMode == True:
                    godMode = False
                    godModeSaved = True
                    

        pygame.display.update()

    pygame.mixer.Channel(0).set_volume(0.5)
    
    speed=difficulty*5

    fruitColour=green
    lastCommand=0
    score=0
    length=1
    gameOver=False
    gameClosed=False
    fruitPresent=False
    active=True
    x = int(width/2)*block
    y = int(height/2)*block
    
    x_change = 0
    y_change = 0
    
    snakeBody=[[] for x in range(width*height)]
    updateBody(x,y,snakeBody,active)
    
    active=False
    while gameOver==False:

        while gameClosed==True:
            pygame.mixer.Channel(0).set_volume(0.1)
            global highscore
            if score > highscore:
                highscore = score
                file = open("highscore.txt","r")
                savedHighscore = int(file.read())
                file.close()
                if highscore > savedHighscore:
                    file = open("highscore.txt","w")
                    file.write(str(highscore))
                    file.close()

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
                elif event.key == pygame.K_e:
                    gameClosed = True
                elif event.key == pygame.K_SPACE:
                    pygame.mixer.Channel(0).set_volume(0.1)
                    paused()
            active=True
        x += x_change
        y += y_change
        screen.fill(black)
        
        if godMode == True or walls == False:
            if x >= block*width:
                x = 0
            elif x <= -block:
                x = block*width-block
            if y >= block*height:
                y = 0
            elif y <= -block:
                y = block*height-block
        else:
            if x >= block*width or x <= -block:
                gameClosed = True
            if y >= block*height or y <= -block:
                gameClosed = True

        updateBody(x,y,snakeBody,active)
        # print(snakeBody[0])
        
        if snakeBody[0] in snakeBody[1:length] and godMode == False:
            gameClosed=True

        if fruitPresent==False:
            fruitArray=[x for x in gridArray if x not in snakeBody[0:score+1]]
            position=random.randint(0,len(fruitArray)-1)
            fruitWidth=fruitArray[position][0]
            fruitHeight=fruitArray[position][1]
            fruitPresent=True

        if x==fruitWidth and y==fruitHeight:
            
            if fruitColour == green:
                pygame.mixer.Channel(1).play(sound)
                length+=1
                score+=1
            elif fruitColour == cyan:
                pygame.mixer.Channel(1).play(sound)
                length+=5
                score+=5
            elif fruitColour == pink:
                pygame.mixer.Channel(1).play(sound)
                length+=10
                score+=10
            elif fruitColour == indigo:
                pygame.mixer.Channel(1).play(sound)
                length+=15
                score+=15
            elif fruitColour == orange:
                pygame.mixer.Channel(1).play(sound)
                length+=20
                score+=20
            if uniqueList(snakeBody)>=25:
                randomFactor=random.randint(0,1000)
                if randomFactor <= 800:
                    fruitColour=green
                elif randomFactor <= 900:
                    fruitColour=cyan
                elif randomFactor <= 960:
                    fruitColour=pink
                elif randomFactor <= 999:
                    fruitColour=indigo
                elif randomFactor == 1000:
                    fruitColour=orange
            fruitPresent=False
            
        pygame.draw.rect(screen, fruitColour, [fruitWidth, fruitHeight, block, block])
        
        if length>1:
            printBody(length,snakeBody)
        pygame.draw.rect(screen, red2, [x, y, block, block])
                
        scoreStr="SCORE: "+str(score)
        highscoreStr="HIGHSCORE: "+str(highscore)
        Message(highscoreStr, white,20,screenWidth-120,10)
        Message(scoreStr,white,20,10,10)
        Message("Press SPACE to pause/unpause, Q to quit or E to Auto-End",white,20,10,screenHeight-20)
        if godMode == True:
            Message("God mode: enabled",white,20,10,25)
        else:
            Message("God mode: disabled",white,20,10,25)       
        pygame.display.update()
        clock.tick(speed)    

    pygame.quit()
    exit()
    
GAME_LOOP()