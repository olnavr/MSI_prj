#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Door:
    def __init__(self, x, y, rx, ry, status):
        self.status = status
        self.cells = []# 2 kratki z których są dostępne dzwi *|*
        if self.status == 'v':# dzwi pionowe | pozycja kreski
            self.x = [x, x]
            self.y = [y, y + 1]
        elif self.status == 'h':# dzwi poziome --
            self.x = [x, x + 1]
            self.y = [y, y]
        self.addCell()

    def addCell(self):# oblicznie cells
        if self.status == 'v':
            self.cells.append([self.x[0] - 1, self.y[0]])
            self.cells.append([self.x[0], self.y[0]])
        elif self.status == 'h':
            self.cells.append([self.x[0], self.y[0] - 1])
            self.cells.append([self.x[0], self.y[0]])
        #print(self.cels)
	#zmiana x,y
    def move(self, x, y):
        self.x = x
        self.y = y

    def update(self, status):
        self.status = status

    def info(self):
        print('door ', self.x, self.y, self.status)