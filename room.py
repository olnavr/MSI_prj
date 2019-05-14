#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import seed, choice, random, randint
from door import Door
from Obstacle import Obstacle, MovingObstacle
from copy import deepcopy

LOOP_LIMIT = 500

class Room:
    def __init__(self, width, length, obs_st, obs_mov):
        self.width = width
        self.length = length
        self.status = '1'
        self.n_c = obs_st
        self.obstacles_c = []
        self.obstacles_mov = []
        self.n_mov = obs_mov
        self.origin = [0, 0]
        self.anti_origin = [length, width]

    def addConstObstacle(self, non_block):
        g = deepcopy(non_block)
        l = len(g)
        c = 0
        while len(g) < l + self.n_c and c < LOOP_LIMIT:
            x = randint(self.origin[0], self.anti_origin[0]-1)
            y = randint(self.origin[1], self.anti_origin[1]-1)
            if sum([e == [x, y] for e in g]) == 0:
                g.append([x, y])
                self.obstacles_c.append(Obstacle(x, y, 'n'))
            c += 1

    def addMovingObstacle(self, non_block):
        g = deepcopy(non_block)
        for oc in self.obstacles_c:
            g.append(oc.cells)
        l = len(g)
        c = 0
        while len(g) < l + self.n_mov and c < LOOP_LIMIT:
            x = randint(self.origin[0], self.anti_origin[0] - 1)
            y = randint(self.origin[1], self.anti_origin[1] - 1)
            if sum([e == [x, y] for e in g]) == 0:
                g.append([x, y])
                s = 'v'
                if random() > 0.5:
                    s = 'h'
                mo = MovingObstacle(x, y, self.origin, self.anti_origin, s)
                mo.calcLimits(g)
                self.obstacles_mov.append(mo)
            c += 1

    def update(self):
        for ob in self.obstacles_mov:
            ob.update()
            print(ob.cells)
