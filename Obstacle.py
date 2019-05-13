#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import seed, choice, random, randint

class Obstacle:
    def __init__(self, x, y, status):
        self.cells = [x,y]
        self.status = status


    def update(self, status):
        self.status = status