#!/usr/bin/env python
# -*- coding: utf-8 -*-
from room import Room
from door import Door
from random import seed, choice, random, randint
from operator import add, sub
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from copy import deepcopy
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.animation as animation

class Wourld:
    def __init__(self, r_list, rand_seed):
        seed(rand_seed)
        self.rooms = []
        self.doors = []
        self.agents = []
        self.addRooms(r_list)

    def addRooms(self, r_list):
        for r in r_list:
            self.rooms.append(Room(*r))

    def calcOrigin(self, r1, r2):
        val = -1
        if random() > 0.5:
            val = 'h'
            self.rooms[r2].origin[0] = choice(list(range(self.rooms[r1].length)))
            self.rooms[r2].origin[1] = self.rooms[r1].width
        else:
            val = 'v'
            self.rooms[r2].origin[0] = self.rooms[r1].length
            self.rooms[r2].origin[1] = choice(list(range(self.rooms[r1].width)))

        if random() > 0.5:
            self.rooms[r2].anti_origin = list(
                map(add, self.rooms[r2].origin, [self.rooms[r2].length, self.rooms[r2].width]))
        else:
            self.rooms[r2].anti_origin = list(
                map(add, self.rooms[r2].origin, [self.rooms[r2].width, self.rooms[r2].length]))

        self.canvas_size = [max(self.rooms[r2].anti_origin[0], self.rooms[r1].anti_origin[0]),
                            max(self.rooms[r2].anti_origin[1], self.rooms[r1].anti_origin[1])]
        return val

    def addExternalDoor(self, d, r):
        dp = []
        s = ''
        x = [self.rooms[r].origin[0], self.rooms[r].anti_origin[0]]
        y = [self.rooms[r].origin[1], self.rooms[r].anti_origin[1]]
        x1 = [self.rooms[r].origin[0], self.rooms[r].anti_origin[0]-1]
        y1 = [self.rooms[r].origin[1], self.rooms[r].anti_origin[1]-1]
        if self.doors[d].status == 'v':
            x.remove(self.doors[d].x[0])
        elif self.doors[d].status == 'h':
            y.remove(self.doors[d].y[0])
        if random() > 0.5:
            s = 'v'
            dp = [choice(x), randint(*y1)]
        else:
            s = 'h'
            dp = [randint(*x1), choice(y)]
        self.doors.append(Door(*dp, *self.rooms[r].anti_origin, s))

    def addInternalDoor(self, r1, r2, s):
        x, y = [0], [0]
        r = 0
        dp = [0, 0]
        if self.rooms[r1].status == '0':
            r = r1
            x = [self.rooms[r2].origin[0], min(self.rooms[r1].anti_origin[0], self.rooms[r2].anti_origin[0])]
            y = [self.rooms[r2].origin[1], min(self.rooms[r1].anti_origin[1], self.rooms[r2].anti_origin[1])]
        elif self.rooms[r2].status == '0':
            r = r2
            x = [self.rooms[r1].origin[0], min(self.rooms[r1].anti_origin[0], self.rooms[r2].anti_origin[0])]
            y = [self.rooms[r1].origin[1], min(self.rooms[r1].anti_origin[1], self.rooms[r2].anti_origin[1])]
        if s == 'v':
            dp = [choice(x), randint(y[0],y[-1]-1)]
        elif s == 'h':
            dp = [randint(x[0], x[-1]-1), choice(y)]
        self.doors.append(Door(*dp, *self.rooms[r].anti_origin, s))

    def combine2Rooms(self):
        self.rooms[0].origin = [0,0]
        self.rooms[1].origin = [0,0]
        if random() > 0.5:
            p = self.calcOrigin(0, 1)
            self.rooms[0].status = '0'
            self.addInternalDoor(0, 1, p)
        else:
            p = self.calcOrigin(1, 0)
            self.rooms[1].status = '0'
            self.addInternalDoor(1, 0, p)
        self.addExternalDoor(0, 1)
        self.addObstacles()

    def addObstacles(self):
        u = []
        for d in self.doors:
            for c in d.cells:
                u.append(c)
        for r in self.rooms:
            r.addConstObstacle(u)
            r.addMovingObstacle(u)

    def addAgents(self):
        pass

    def update(self):
        for r in self.rooms:
            r.update()

    def info(self):
        for r in self.rooms:
            r.info()
            print("---------------")
