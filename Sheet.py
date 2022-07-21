import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import math

from Brick import Brick

class Sheet:

    def __init__(self):
        self.x = 500
        self.y = 300
        self.llist = {2: 300, 4: 300, 7: 150, 8: 550, 12: 300, 16: 300, 17: 100, 19: 100,22: 350, 24: 350, 27: 100,29: 100}
        self.rlist = {3: 300, 5: 100, 9: 250, 10: 350, 15: 100, 19: 500, 20: 300, 25: 150,  28: 200,30: 300, }
        self.lindex = 0
        self.rindex = 0
        self.time = 0
        self.lbricks = []
        self.rbricks = []

        for key in  self.llist.keys():
            self.lbricks.append(Brick("Left",key,y=self.llist[key]))
        for key in self.rlist.keys():
            self.rbricks.append(Brick("Right", key, x = 800, y=self.rlist[key]))

    def get_bricks(self):
        return self.bricks

    def next_brick(self,time):
        bricks = []

        if time in self.llist.keys():
            self.lindex += 1
            bricks.append(self.lbricks[self.lindex - 1])
        if time in self.rlist.keys():
            self.rindex += 1
            bricks.append(self.rbricks[self.rindex - 1])
        return bricks


    def next(self, time):
        if time in self.llist.keys():
            self.time = time
        if time in self.rlist.keys():
            self.time = time
        return self.time

    def get_position(self):
        return self.x,self.y