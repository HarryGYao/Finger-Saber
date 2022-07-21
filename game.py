import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import math
from Brick import Brick
from Sheet import Sheet
from Button import Button

pygame.init()
# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Finger Saber")
clock = pygame.time.Clock()
# Webcam
cap = cv2.VideoCapture(2)
cap.set(3, width)  # width
cap.set(4, height)  # height


sheet = Sheet()
start_button = Button(530,350,pygame.image.load('Resources/start.png').convert_alpha(),1)
restart_button = Button(530,350,pygame.image.load('Resources/restart.png').convert_alpha(),1)



light_saber = pygame.image.load('Resources/light_saber.png').convert_alpha()
rect_light_saber = light_saber.get_rect()
rect_light_saber.x, rect_light_saber.y = 0, 0




# Variables

score = 0
startTime = time.time()
totalTime = 34

# Detector
detector = HandDetector(detectionCon=0.5, maxHands=2)

current_timer = 0
last_index = 0
# Main loop
start = True
bricks = []
font = pygame.font.Font('Resources/QTDeuce.otf', 50)
combo = 0
menu = True
font_menu = pygame.font.Font('Resources/QTDeuce.otf', 150)
first_end = True
while start:
    # Get Events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    current_timer = time.time() - startTime
    timeRemain = int(totalTime - int(current_timer))
    index = sheet.next(totalTime-timeRemain)
    if last_index < index:
        bricks.extend(sheet.next_brick(int(current_timer)))

    last_index = index
    bricks = [x for x in bricks if not x.done] #collect done

    if menu:
        window.fill((0, 0, 0))
        texttitle = font_menu.render('Finger Saber', True, (255, 215, 0))
        window.blit(texttitle, (300, 150))
        clicked = start_button.draw(window)
        if clicked:
            menu = False
            sheet = Sheet()
            startTime = time.time()
            bricks = []
            current_timer = 0
            last_index = 0
            combo = 0
            score = 0
            pygame.mixer.music.load('Resources\Chocobo.mp3')
            pygame.mixer.music.play()

    else:

        if timeRemain < 0:

            window.fill((0, 0, 0))

            textScore = font.render(f'Your Score: {score}', True,  (255, 215, 0))
            textTime = font.render(f'Time UP', True,  (255, 215, 0))
            window.blit(textScore, (450, 250))
            window.blit(textTime, (530, 175))
            clicked = restart_button.draw(window)
            if first_end:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('Resources\ictory.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                first_end = False
            # reset
            if clicked:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('Resources\Chocobo.mp3')
                pygame.mixer.music.play()
                first_end = True
                sheet = Sheet()
                startTime = time.time()
                bricks = []
                current_timer = 0
                last_index = 0
                combo = 0
                score = 0

        else:
            # OpenCV
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands = detector.findHands(img, flipType=False, draw=False)
            # hands, img = detector.findHands(img, flipType=False) # if want to see the frame

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            # window.blit(brick.img, brick.rect)
            for brick in  bricks:
                brick.draw(window,current_timer)
            if not hands: # no hand
                for brick in bricks:
                    if brick.status == 0:
                        if abs(current_timer - brick.timestamp) > 2:
                            brick.miss(current_timer)
                        score += brick.score
            for hand in  hands:
                x, y, z = hand['lmList'][8]
                for brick in bricks:

                    if brick.status == 0:
                        if  brick.bounding.collidepoint(x, y): # only check once, this if statement is important
                            brick.hit()
                        if  brick.rect.collidepoint(x, y):

                            if brick.hit_bounding:
                                if abs(current_timer - index) < 0.2:
                                    combo = 0
                                    brick.error(current_timer)
                                elif abs(current_timer - index) < 0.6:
                                    combo += 1
                                    brick.good(current_timer)
                                elif abs(current_timer - index) < 1:
                                    combo += 1
                                    brick.perfect(current_timer)
                                else:
                                    combo += 1
                                    brick.good(current_timer)
                            else:
                                # brick.resetBox()
                                combo = 0
                                brick.error(current_timer)
                        if abs(current_timer - brick.timestamp) >1.5 :
                            combo = 0
                            brick.miss(current_timer)
                        score += brick.score


                x2, y2, z2 = hand['lmList'][5]
                rect_light_saber.x, rect_light_saber.y = x, y
                x_ = (x-x2)
                y_ = (y-y2)
                rotated_image = light_saber
                if y_:
                    angle = np.rad2deg(math.atan(x_ / y_))
                    rotated_image = pygame.transform.rotate(light_saber, angle)
                    if y > y2:
                        rotated_image = pygame.transform.rotate(rotated_image, 180)
                        rect_light_saber.y -= rotated_image.get_height()
                    if x >x2:
                        rect_light_saber.x -= rotated_image.get_width()
                window.blit(rotated_image, rect_light_saber)



            textScore = font.render(f'Score: {score}', True,  (255, 215, 0))
            textTime = font.render(f'Time: {timeRemain}', True,  (255, 215, 0))
            textCombo = font.render(f'Combo: {combo}', True,  (255, 215, 0))
            window.blit(textScore, (35, 35))
            window.blit(textCombo, (35, 200))
            window.blit(textTime, (1000, 35))

    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(60)
    # print(clock.get_fps())