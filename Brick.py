import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import math

class Brick:

    def __init__(self, direction,timestamp = 0, x = 500,y=300):
        self.direction = direction
        self.img = pygame.image.load('Resources/box.png').convert_alpha()
        self.correct_img = pygame.image.load('Resources/perf.png').convert_alpha()
        self.good_img = pygame.image.load('Resources/good.png').convert_alpha()
        self.error_img =pygame.image.load('Resources/error.png').convert_alpha()
        self.miss_img = pygame.image.load('Resources/miss.png').convert_alpha()
        self.bound_img = pygame.image.load('Resources/boundary.png').convert_alpha()

        self.correct_sound = pygame.mixer.Sound("Resources/correct.wav")
        self.error_sound = pygame.mixer.Sound("Resources/error.wav")

        self.correct_sound.set_volume(0.2)
        self.error_sound.set_volume(0.4)

        self.rect = self.img.get_rect()
        self.zoom = self.img.get_rect()
        self.bounding = self.img.get_rect()
        self.bounding.x, self.bounding.y = x - self.bounding.width, y
        if self.direction == "Right":
            self.img = pygame.transform.rotate(self.img, 180)
            self.bounding.x, self.bounding.y = x + self.bounding.width, y
        self.hit_bounding = False
        self.rect.x, self.rect.y = x, y
        self.timestamp = timestamp
        self.done =False
        self.status = 0 # 0-not done 1-perfect 2-good 3- error 4-missing
        self.check_box_x, self.check_box_y  = self.rect.x, self.rect.y
        self.score = 0
        self.alpha = 255
        self.scale_x = 0
        self.scale_y = 0


    def resetBox(self):
        self.hit_bounding = False
        self.rect.x = 0
        self.rect.y = 0
        self.bounding.x, self.bounding.y = self.rect.x - self.bounding.width, self.rect.y


    def next(self,x,y):
        # self.hit_bounding = False
        self.rect.x = x
        self.rect.y = y
        self.check_box_x, self.check_box_y = self.rect.x, self.rect.y
        self.bounding.x, self.bounding.y = self.rect.x - self.bounding.width, self.rect.y

    def hit(self):
        self.hit_bounding = True

    def draw(self,window, time):

        if self.status == 0:


            self.scale_x += 10
            self.scale_y += 10
            if self.scale_x > 128:
                self.scale_x = 128
                self.scale_y = 128
            self.zoom.x= self.rect.x+((128 - self.scale_x)/2)
            self.zoom.y = self.rect.y+((128 - self.scale_x) / 2)

            image = pygame.transform.scale(self.img, (self.scale_x,self.scale_y ))
            window.blit(image, self.zoom)
            window.blit(self.bound_img, self.rect)
        elif self.status == 1:
            self.alpha *= 0.94
            self.correct_img.set_alpha(self.alpha)
            window.blit(self.correct_img, self.rect)
            self.done =  abs(time - self.timestamp) >0.7
        elif self.status == 2:
            self.alpha *= 0.94
            self.good_img.set_alpha(self.alpha)
            window.blit(self.good_img, self.rect)
            self.done =  abs(time - self.timestamp) >0.7
        elif self.status == 3:
            self.alpha *= 0.94
            self.error_img.set_alpha(self.alpha)
            window.blit(self.error_img, self.rect)
            self.done =  abs(time - self.timestamp) >0.7
        elif self.status == 4:
            self.alpha *= 0.94
            self.miss_img.set_alpha(self.alpha)
            window.blit(self.miss_img, self.rect)
            self.done =  abs(time - self.timestamp) >0.7 #show 1 second

    def perfect(self,time):
        self.correct_sound.play()
        self.timestamp = time
        self.status = 1
        self.score = 100

    def good(self,time):
        self.correct_sound.play()
        self.timestamp = time
        self.status = 2
        self.score = 50

    def error(self,time):
        self.error_sound.play()
        self.timestamp = time
        self.status = 3
        self.score = -50

    def miss(self,time):
        self.error_sound.play()
        self.timestamp = time
        self.status = 4
        self.score = -100