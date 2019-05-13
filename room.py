#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import seed, choice, random, randint
from door import Door
from Obstacle import Obstacle

class Room:
    def __init__(self, width, length, y, obj_num):
        self.width = width
        self.length = length
        self.status = '1'
        self.obstacles = []
        self.origin = [0, 0]
        self.anti_origin = [length, width]

    def addObstacle(self, num):
        g = []
        for i in range(num):
            x = randint(self.origin[0], self.anti_origin[0]-1)
            y = randint(self.origin[1], self.anti_origin[1]-1)
            #g.append([x, y])
            self.obstacles.append(Obstacle(x, y, 'n'))
        #print(g)

    def update(self):
        for ob in self.obstacles:
            ob.update()
