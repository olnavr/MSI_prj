#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import seed, choice, random, randint
from copy import deepcopy
import matplotlib; matplotlib.use("TkAgg")

#pszeszkoda nieruchoma
class Obstacle:
    def __init__(self, x, y, status):
        self.cells = [x, y]
        self.status = status

    def update(self, status):
        self.status = status

		#pszeszkoda ruchoma
class MovingObstacle:
    def __init__(self, x, y, r_orig, r_anti_orig, status):
        self.cells = [x, y]# pozycja przesz.
        self.status = status # ruch poziomy czy pionowy
        self.way = 1
        self.N = 0  # liczba pól, po których chodzi przeszkoda
        self.T = 0  # okres ruchu przeszkody
        self.b = 0  # bias - przesunięcie (faza początkowa) okresowego ruchu przeszkody
        self.history = []
        if self.status == 'v':
            self.limits = [r_orig[1]-1, r_anti_orig[1]]
        elif self.status == 'h':
            self.limits = [r_orig[0]-1, r_anti_orig[0]]

    def calcLimits(self, obs):#obliczenie ograniczeń ruchu
        g = [self.limits[0]]
        inx = 0
        if self.status == 'v':
            for o in obs:
                if o[0] == self.cells[0]:
                    g.append(o[1])
            g.append(self.limits[1])
            g.append(self.cells[1])
            g.sort()
            inx = g.index(self.cells[1])
        elif self.status == 'h':
            for o in obs:
                if o[1] == self.cells[1]:
                    g.append(o[0])
            g.append(self.limits[1])
            g.append(self.cells[0])
            g.sort()
            inx = g.index(self.cells[0])
        if inx == 0:
            self.limits = [g[inx], g[1]]
        elif inx == len(g)-1:
            self.limits = [g[0], g[-1]]
        else:
            self.limits = [g[inx-1], g[inx+1]]

        self.N = self.limits[1] - self.limits[0] - 1
        self.T = 2*(self.N - 1)
        if self.status == 'v':
            self.b = self.cells[1] - self.limits[0] - 1
        elif self.status == 'h':
            self.b = self.cells[0] - self.limits[0] - 1

    # sprawdzenie czy w momencie t przeszkoda porusza się w prawo (status=h) lub w górę (status=v)
    def move_right_up(self, t):
        return

    def is_in(self, i, t):
        return (t == self.T - i - self.b) or (self == ((self.T + i - self.b) % self.T))

    def update(self): # obliczanie następnego kroku
        if self.status == 'v':
            if self.cells[1] == self.limits[0]+1:
                self.way = 1
            elif self.cells[1] == self.limits[1]-1:
                self.way = -1
            self.cells[1] = self.cells[1] + self.way
        elif self.status == 'h':
            if self.cells[0] == self.limits[0]+1:
                self.way = 1
            elif self.cells[0] == self.limits[1]-1:
                self.way = -1
            self.cells[0] = self.cells[0] + self.way
        self.history.append(deepcopy(self.cells))
