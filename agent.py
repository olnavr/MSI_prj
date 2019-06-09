#!/usr/bin/env python
# -*- coding: utf-8 -*-


# sprawdzenie czy punkt jest ścianą
def is_wall(next_point, w, current_room):
    if next_point[0] < w.rooms[current_room].origin[0] or \
            next_point[0] > w.rooms[current_room].anti_origin[0] - 1 or \
            next_point[1] < w.rooms[current_room].origin[1] or \
            next_point[1] > w.rooms[current_room].anti_origin[1] - 1:
        return True
    else:
        return False


class Agent:
    def __init__(self, start_point, targets):
        self.current_point = start_point
        self.targets = targets
        self.target1_reached = False
        self.track = [[], []]
        self.hypothetical_track = []
        self.t_max = 50  # maksymalna długość ścieżki
        self.t = 0
        self.t_max_tries_max = 5
        self.t_max_tries = 0
        self.first_move = True
        self.back_to_first_move = False

    # główny algorytm rekurencyjny
    def backtracking_algorithm(self, w):
        neighbors = self.get_neighbors()  # pozyskanie sąsiadów badanego w danym momencie punktu
        current_time = self.t
        current_move_first = self.first_move
        if self.first_move:
            self.first_move = False

        # sprawdzenie który pokój sprawdza teraz agent
        if self.target1_reached:
            current_room = 1
        else:
            current_room = 0
        current_target = self.targets[current_room]  # aktualny cel

        # sprawdzenie czy aktualny cel został już osiągnięty
        if self.current_point == current_target:
            self.target1_reached = True
            self.track[current_room].insert(0, self.current_point)
            self.door_pass(w)
            self.t = current_time + 1
            return True

        if self.t_max_tries < self.t_max_tries_max:

            if self.t < self.t_max:

                # sprawdzenie ruchu w prawo
                if self.current_point[0] < current_target[0] and \
                        not self.is_obstacle(w, current_room, neighbors[0], current_time) and \
                        not is_wall(neighbors[0], w, current_room) and \
                        not neighbors[0] in self.hypothetical_track and \
                        (not self.back_to_first_move or current_move_first):
                    if self.new_step(current_time, neighbors, 0, w, current_room):
                        return True

                # sprawdzenie ruchu w górę
                if self.current_point[1] < current_target[1] and \
                        not self.is_obstacle(w, current_room, neighbors[1], current_time) and \
                        not is_wall(neighbors[1], w, current_room) and \
                        not neighbors[1] in self.hypothetical_track:
                    if self.new_step(current_time, neighbors, 1, w, current_room):
                        return True

                # sprawdzenie ruchu w lewo
                if self.current_point[0] > current_target[0] and \
                        not self.is_obstacle(w, current_room, neighbors[2], current_time) and \
                        not is_wall(neighbors[2], w, current_room) and \
                        not neighbors[2] in self.hypothetical_track:
                    if self.new_step(current_time, neighbors, 2, w, current_room):
                        return True

                # sprawdzenie ruchu w dół
                if self.current_point[1] > current_target[1] and \
                        not self.is_obstacle(w, current_room, neighbors[3], current_time) and \
                        not is_wall(neighbors[3], w, current_room) and \
                        not neighbors[3] in self.hypothetical_track:
                    if self.new_step(current_time, neighbors, 3, w, current_room):
                        return True

                # podobne sprawdzania ruchów, ale w sytuacji, gdy nie można zmierzać w kierunku celu

                # sprawdzenie ruchu w prawo
                if not self.is_obstacle(w, current_room, neighbors[0], current_time) and \
                        not is_wall(neighbors[0], w, current_room) and \
                        not neighbors[0] in self.hypothetical_track:
                    if self.new_step(current_time, neighbors, 0, w, current_room):
                        return True

                # sprawdzenie ruchu w górę
                if not self.is_obstacle(w, current_room, neighbors[1], current_time) and \
                        not is_wall(neighbors[1], w, current_room) and \
                        not neighbors[1] in self.hypothetical_track:
                    if self.new_step(current_time, neighbors, 1, w, current_room):
                        return True

                # sprawdzenie ruchu w lewo
                if not self.is_obstacle(w, current_room, neighbors[2], current_time) and \
                        not is_wall(neighbors[2], w, current_room) and \
                        not neighbors[2] in self.hypothetical_track:
                    if self.new_step(current_time, neighbors, 2, w, current_room):
                        return True

                # sprawdzenie ruchu w dół
                if not self.is_obstacle(w, current_room, neighbors[3], current_time) and \
                        not is_wall(neighbors[3], w, current_room) and \
                        not neighbors[3] in self.hypothetical_track:
                    if self.new_step(current_time, neighbors, 3, w, current_room):
                        return True
            else:
                self.t_max_tries = self.t_max_tries + 1
        else:
            self.back_to_first_move = True
        return False

    # funkcja do pozyskania sąsiadów aktualnie rozpatrywanego punktu
    def get_neighbors(self):
        neighbors = ([])
        neighbors.append([self.current_point[0] + 1, self.current_point[1]])
        neighbors.append([self.current_point[0], self.current_point[1] + 1])
        neighbors.append([self.current_point[0] - 1, self.current_point[1]])
        neighbors.append([self.current_point[0], self.current_point[1] - 1])
        return neighbors

    # funkcja służąca do przechodzenia przez drzwi
    def door_pass(self, w):
        if self.current_point == w.doors[0].cells[0]:
            self.current_point = w.doors[0].cells[1]
        else:
            self.current_point = w.doors[0].cells[0]

    # wykonanie kolejnego kroku
    def new_step(self, current_time, neighbors, neighbor, w, current_room):
        self.hypothetical_track.append(self.current_point)
        self.t = current_time + 1
        previous_point = self.current_point
        self.current_point = neighbors[neighbor]
        if self.back_to_first_move:
            self.back_to_first_move = False
        if self.backtracking_algorithm(w):
            self.track[current_room].insert(0, previous_point)
            return True
        else:
            self.hypothetical_track.remove(previous_point)
            self.current_point = previous_point
            return False

    # sprawdzenie czy w punkcie nastąpi kolizja z przeszkodą
    def is_obstacle(self, w, current_room, next_point, current_time):
        for oc in w.rooms[current_room].obstacles_c:
            if next_point == oc.cells:
                return True

        for om in w.rooms[current_room].obstacles_mov:
            if om.T == 0:
                if next_point == om.cells:
                    return True
            else:
                tc = current_time % om.T
                tn = (current_time + 1) % om.T
                if om.status == 'v':
                    for i in range(0, om.N):
                        if (next_point == [om.cells[0], om.cells[1] - om.b + i]) and \
                                (((not om.move_right_up(tc) and (next_point[1] > self.current_point[1])) or (om.move_right_up(tc) and (next_point[1] < self.current_point[1]))) and om.is_in(i, tc) or
                                 om.is_in(i, tn)):
                            return True
                elif om.status == 'h':
                    for i in range(0, om.N):
                        if (next_point == [om.cells[0] - om.b + i, om.cells[1]]) and \
                                (((not om.move_right_up(tc) and (next_point[0] > self.current_point[0])) or (om.move_right_up(tc) and (next_point[0] < self.current_point[0]))) and om.is_in(i, tc) or
                                 om.is_in(i, tn)):
                            return True
        return False
