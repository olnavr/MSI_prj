#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wourld import Wourld
from room import Room
from anime import Anime
from agent import Agent

def main(args):
    r_list = [[12, 11, 5, 3], [17, 7, 5, 3]]
    anim = True
    n_tests = 50  # liczba testów
    opt_cnt = 0  # licznik światów, w których została znaleziona trasa najbardziej optymalna
    fail_cnt = 0  # licznik światów, w których nie udało się znaleźć trasy
    mean_exc = 0  # średnia bezwzględna nadmiarowość trasy
    random_seed = 1
    for i in range(n_tests):
        w = Wourld(r_list, random_seed)
        w.combine2Rooms()
        w.calcTargets()
        agent = Agent(w.agent_start_point, w.targets)
        if not agent.backtracking_algorithm(w):
            print(i, w.shortest_route, "NIE UDAŁO SIĘ ZNALEŹĆ ŚCIEŻKI")
            fail_cnt = fail_cnt + 1
        else:
            if not agent.backtracking_algorithm(w):
                print(i, w.shortest_route, "NIE UDAŁO SIĘ ZNALEŹĆ ŚCIEŻKI")
                fail_cnt = fail_cnt + 1
            else:
                track = agent.track[0] + agent.track[1]
                len_track = len(track)
                # iteration, Shortest track,robot track
                if len_track == w.shortest_route:
                    opt_cnt = opt_cnt + 1
                print(i, w.shortest_route, len(track))
                mean_exc = mean_exc + len_track - w.shortest_route
                if anim:
                    anime = Anime(w, agent, 'm')
                    input()
        random_seed = random_seed + 1
    mean_exc = mean_exc/n_tests
    print("- liczba testów: ", n_tests)
    print("- liczba tras najbardziej optymalnych: ", opt_cnt)
    print("- liczba tras nieznalezionych: ", fail_cnt)
    print("- średni współczynnik bezwzględnej nadmiarowości tras: ", mean_exc)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
