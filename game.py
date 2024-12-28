import pygame
from time import sleep
import mediapipe as mp
import os
import cv2
import cvzone
import numpy as np
from pynput.keyboard import Key, Controller
from cvzone.HandTrackingModule import HandDetector

W1=cv2.imread(".\Assets\wheel1.png",cv2.IMREAD_UNCHANGED)
W1=cv2.resize(W1,(280,280))
W1=cvzone.rotateImage(W1,45)

keyboard=Controller()

cap=cv2.VideoCapture(0)
cap.set(3,900)
cap.set(4,420)
detector=HandDetector(detectionCon=0.8,maxHands=1)
flag=False
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('.\Assets\music.mp3')
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
gameWindow = pygame.display.set_mode((500,750))
pygame.display.set_caption("Astrododge")
FONT = pygame.font.SysFont('Arial', 100)
ASTROID_SPEED = 30
SCORE = 0
GAME_OVER = False
clock = pygame.time.Clock()
backgroundImage = pygame.image.load(".\Assets\\bg.jpg").convert()
backgroundImage2 = pygame.image.load(".\Assets\\bg3.jpg").convert()
ROCKET_X = 250
ASTROID = pygame.image.load(".\Assets\\astroid.png").convert_alpha()
ASTROID = pygame.transform.scale(ASTROID,(80,80))
ASTROID_X = ROCKET_X
ASTROID_Y = -750
backgroundImage_y1 = 0
backgroundImage2_y2 = -750
backgroundImage = pygame.transform.scale(backgroundImage,(500,750))
backgroundImage2 = pygame.transform.scale(backgroundImage2,(500,750))
i=0
pygame.mixer.music.play()

while not GAME_OVER : 
    _,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)

    if hands:
        hand=hands[0]['lmList']
        arm1=hand[8]
        arm2=hand[5]
        org=hand[0]
        radians=np.arctan2(org[1]-arm2[1],org[0]-arm2[0])-np.arctan2(arm1[1] - arm2[1], arm1[0] - arm2[0])
        angle=round(np.abs(radians*180/np.pi),2)
        cvzone.putTextRect(img,f'{angle}',(org[1]+10,org[0]+10),1,2)
    
        if angle<=180 and flag==True:
            W1=cvzone.rotateImage(W1,-90)
            flag=False
        elif angle>180 and flag==False:
            W1=cvzone.rotateImage(W1,90)
            flag=True
        
        if angle<=180:
            keyboard.press(Key.right)
            if ( ROCKET_X <= 340):
                    ROCKET_X += 70
            print ("ROCKET X COORDINATES: %s" % ROCKET_X)
            keyboard.release(Key.right)
            
        else :
            keyboard.press(Key.left)
            if (ROCKET_X > 40):
                ROCKET_X -= 70
            elif ROCKET_X <=40 :
                ROCKET_X = 10
            print ("ROCKET X COORDINATES: %s" % ROCKET_X)
            keyboard.release(Key.left)
        
        img=cvzone.overlayPNG(img,W1,[180,150])
        
        cv2.imshow('Hand Tracking', img)
        cv2.moveWindow('Hand Tracking',800,200)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    gameWindow.blit(backgroundImage,(0,backgroundImage_y1))
    gameWindow.blit(backgroundImage2,(0,backgroundImage2_y2))
    gameWindow.blit(ASTROID,(ASTROID_X,ASTROID_Y))
    gameWindow.blit(pygame.image.load(f".\Assets\\rockets\\rocket{i+1}.gif"),(ROCKET_X,500))
    
    pygame.display.flip()
    backgroundImage_y1 += 50
    backgroundImage2_y2 += 50
    ASTROID_Y += ASTROID_SPEED

    if ASTROID_Y >= 750 :
        ASTROID_Y = 0
        ASTROID_X = ROCKET_X
        ASTROID_SPEED+=5
    if backgroundImage_y1 >= 750 :
        backgroundImage_y1 = -750
    elif backgroundImage2_y2 >= 750 :
        backgroundImage2_y2 = -750
    i=(i+1)%8
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            GAME_OVER = True
            continue
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                if (ROCKET_X > 40):
                    ROCKET_X -= 70
                elif ROCKET_X <=40 :
                    ROCKET_X = 10
                print ("ROCKET X COORDINATES: %s" % ROCKET_X)
            if (event.key == pygame.K_RIGHT):
                if ( ROCKET_X <= 340):
                    ROCKET_X += 70
                print ("ROCKET X COORDINATES: %s" % ROCKET_X)
    if ASTROID_Y in range(500,751) and ASTROID_X in range(ROCKET_X,ROCKET_X+91): 
       GAME_OVER = True
    if GAME_OVER == False:
        clock.tick(10)
        SCORE +=0.1
    else:
        try:
            gameWindow.blit(pygame.image.load(".\Assets\ASTRODODGE.jpg").convert(),(0,0))
            text = FONT.render(f"{round(SCORE,2)}", True, (215, 215, 0))
            gameWindow.blit(text,(200,200))
            pygame.display.flip()
            pygame.mixer.music.stop()
            sleep(5)
        except Exception:
            pass
