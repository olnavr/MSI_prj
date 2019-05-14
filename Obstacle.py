#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import seed, choice, random, randint

class Obstacle:
    def __init__(self, x, y, status):
        self.cells = [x, y]
        self.status = status

    def update(self, status):
        self.status = status

class MovingObstacle:
    def __init__(self, x, y, r_orig, r_anti_orig, status):
        self.cells = [x, y]
        self.status = status
        self.way = 1
        if self.status == 'v':
            self.limits = [r_orig[1], r_anti_orig[1]]
        elif self.status == 'h':
            self.limits = [r_orig[0], r_anti_orig[0]]
        #print(self.limits, status)

    def calcLimits(self,obs):
        if self.status == 'v':
            for i in range(*self.limits):
                for j in obs:
                    if j[0] == self.cells[0] and j[1] < self.cells[1]:
                        self.limits[0] = j[1]
                    elif j[0] == self.cells[0] and j[1] > self.cells[1]:
                        self.limits[1] = j[1]
                        print(self.cells, self.limits, self.status)
                        return
        elif self.status == 'h':
            for i in range(*self.limits):
                for j in obs:
                    if j[1] == self.cells[1] and j[0] < self.cells[0]:
                        self.limits[0] = j[0]
                    elif j[1] == self.cells[1] and j[0] > self.cells[0]:
                        self.limits[1] = j[0]
                        print(self.cells, self.limits, self.status)
                        return
        print(self.cells, self.limits, self.status)

    def update(self):
        t = 0
        if self.status == 'v':
            t = self.limits[0] + (self.cells[1] + self.way)% self.limits[1]
            if t == 0:
                self.way = self.way * (-1)
                t = self.limits[0] + (self.cells[1] + 2*self.way) % self.limits[1]
            self.cells[1] = t
        elif self.status == 'h':
            t = self.limits[0] +  (self.cells[0] + self.way) % self.limits[1]
            if t == 0:
                self.way = self.way * (-1)
                t = self.limits[0] + (self.cells[1] + 2*self.way) % self.limits[1]
            self.cells[0] = t

