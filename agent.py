#!/usr/bin/env python
# -*- coding: utf-8 -*-


# sprawdzenie czy punkt jest ścianą
def is_wall(point, w, current_room):
    if point[0] < w.rooms[current_room].origin[0] or \
            point[0] > w.rooms[current_room].anti_origin[0] - 1 or \
            point[1] < w.rooms[current_room].origin[1] or \
            point[1] > w.rooms[current_room].anti_origin[1] - 1:
        return True
    else:
        return False


class Agent:
    def __init__(self, sp, targets):
        self.search_point = sp #[12, 28]  # punkt startowy - DO ZMIANY
        # TRZEBA WPROWADZIĆ WYZNACZANIE PUNKTU STARTOWEGO (searching_point) ORAZ
        # CELÓW W POKOJU 1 I 2 (targets[0] i targets[1]) W POSTACI OGÓLNEJ
        self.targets = targets #[[5, 17], [6, 8]]  # cele - DO ZMIANY
        self.target1_reached = False
        self.track = [[], []]
        self.candidate_track = []
        self.t_max = 50
        self.t = 0

    # główny algorytm rekurencyjny
    def backtracking_algorithm(self, w):
        neighbors = self.get_neighbors()  # pozyskanie sąsiadów badanego w danym momencie punktu
        current_time = self.t

        # sprawdzenie który pokój sprawdza teraz agent
        if self.target1_reached:
            current_room = 1
        else:
            current_room = 0
        current_target = self.targets[current_room]  # aktualny cel

        # sprawdzenie czy aktualny cel został już osiągnięty
        if self.search_point == current_target:
            self.target1_reached = True
            self.track[current_room].insert(0, self.search_point)
            self.door_pass(w)
            self.t = current_time + 1
            return True

        if self.t <= self.t_max:

            # sprawdzenie ruchu w lewo
            if self.search_point[0] < current_target[0] and \
                    not self.is_obstacle(w, current_room, neighbors[0]) and \
                    not is_wall(neighbors[0], w, current_room) and \
                    not neighbors[0] in self.candidate_track:
                if self.new_step(current_time, neighbors, 0, w, current_room):
                    return True

            # sprawdzenie ruchu w górę
            if self.search_point[1] < current_target[1] and \
                    not self.is_obstacle(w, current_room, neighbors[1]) and \
                    not is_wall(neighbors[1], w, current_room) and \
                    not neighbors[1] in self.candidate_track:
                if self.new_step(current_time, neighbors, 1, w, current_room):
                    return True

            # sprawdzenie ruchu w lewo
            if self.search_point[0] > current_target[0] and \
                    not self.is_obstacle(w, current_room, neighbors[2]) and \
                    not is_wall(neighbors[2], w, current_room) and \
                    not neighbors[2] in self.candidate_track:
                if self.new_step(current_time, neighbors, 2, w, current_room):
                    return True

            # sprawdzenie ruchu w dół
            if self.search_point[1] > current_target[1] and \
                    not self.is_obstacle(w, current_room, neighbors[3]) and \
                    not is_wall(neighbors[3], w, current_room) and \
                    not neighbors[3] in self.candidate_track:
                if self.new_step(current_time, neighbors, 3, w, current_room):
                    return True

            # podobne sprawdzania ruchów, ale w sytuacji, gdy nie można zmierzać w kierunku celu

            # sprawdzenie ruchu w lewo
            if not self.is_obstacle(w, current_room, neighbors[0]) and \
                    not is_wall(neighbors[0], w, current_room) and \
                    not neighbors[0] in self.candidate_track:
                if self.new_step(current_time, neighbors, 0, w, current_room):
                    return True

            # sprawdzenie ruchu w górę
            if not self.is_obstacle(w, current_room, neighbors[1]) and \
                    not is_wall(neighbors[1], w, current_room) and \
                    not neighbors[1] in self.candidate_track:
                if self.new_step(current_time, neighbors, 1, w, current_room):
                    return True

            # sprawdzenie ruchu w lewo
            if not self.is_obstacle(w, current_room, neighbors[2]) and \
                    not is_wall(neighbors[2], w, current_room) and \
                    not neighbors[2] in self.candidate_track:
                if self.new_step(current_time, neighbors, 2, w, current_room):
                    return True

            # sprawdzenie ruchu w dół
            if not self.is_obstacle(w, current_room, neighbors[3]) and \
                    not is_wall(neighbors[3], w, current_room) and \
                    not neighbors[3] in self.candidate_track:
                if self.new_step(current_time, neighbors, 3, w, current_room):
                    return True

        return False

    # funkcja do pozyskania sąsiadów aktualnie rozpatrywanego punktu
    def get_neighbors(self):
        neighbors = ([])
        neighbors.append([self.search_point[0] + 1, self.search_point[1]])
        neighbors.append([self.search_point[0], self.search_point[1] + 1])
        neighbors.append([self.search_point[0] - 1, self.search_point[1]])
        neighbors.append([self.search_point[0], self.search_point[1] - 1])
        return neighbors

    # funkcja służąca do przechodzenia przez drzwi - MOŻNA ZMIENIĆ
    def door_pass(self, w):
        if self.search_point == w.doors[0].cells[0]:
            self.search_point = w.doors[0].cells[1]
        else:
            self.search_point = w.doors[0].cells[0]

    # wykonanie kolejnego kroku
    def new_step(self, current_time, neighbors, neighbor, w, current_room):
        self.candidate_track.append(self.search_point)
        self.t = current_time + 1
        previous_point = self.search_point
        self.search_point = neighbors[neighbor]
        if self.backtracking_algorithm(w):
            self.track[current_room].insert(0, previous_point)
            return True
        else:
            self.candidate_track.remove(previous_point)
            self.search_point = previous_point
            return False

    # sprawdzenie czy w punkcie nastąpi kolizja z przeszkodą
    def is_obstacle(self, w, current_room, point):
        for oc in w.rooms[current_room].obstacles_c:
            if point == oc.cells:
                return True
        for om in w.rooms[current_room].obstacles_mov:
            temp1 = self.t % om.T
            temp2 = (self.t+1) % om.T
            if om.status == 'v':
                for n in range(0, om.N):
                    if ((point == [om.cells[0], om.cells[1]-om.b+n]) and  # sytuacja, gdy miną się w kolejnym ruchu
                        (((om.way == -1) and (point[1] > self.search_point[1])) or ((om.way == 1) and
                                                                                    (point[1] < self.search_point[1])))
                        and ((temp1 == om.T-n-om.b) or (temp1 == ((om.T+n-om.b) % om.T)))) or \
                            ((point == [om.cells[0], om.cells[1]-om.b+n]) and ((temp2 == om.T-n-om.b) or  # sytuacja gdy w kolejnym ruchu zajmą to samo pole
                                                                               (temp2 == ((om.T+n-om.b) % om.T)))):
                        return True
            elif om.status == 'h':
                for n in range(0, om.N):
                    if ((point == [om.cells[0]-om.b+n, om.cells[1]]) and
                        (((om.way == -1) and (point[0] > self.search_point[0])) or ((om.way == 1) and
                                                                                    (point[0] < self.search_point[0])))
                        and ((temp1 == om.T-n-om.b) or (temp1 == ((om.T+n-om.b) % om.T)))) or \
                            ((point == [om.cells[0]-om.b+n, om.cells[1]]) and ((temp2 == om.T-n-om.b) or
                                                                               (temp2 == ((om.T+n-om.b) % om.T)))):
                        return True
        return False
