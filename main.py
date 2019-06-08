#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wourld import Wourld
from room import Room
from anime import Anime
from agent import Agent

def main(args):
    r_list = [[12, 11, 5, 3], [17, 7, 5, 3]]
    anim = False
    random_seed = 1
    for i in range(50):
        w = Wourld(r_list, random_seed)
        w.combine2Rooms()
        w.calcTargets()
        agent = Agent(w.agent_sp, w.targets)
        if not agent.backtracking_algorithm(w):
            print("NIE UDAŁO SIĘ ZNALEŹĆ ŚCIEŻKI")
        else:
            if not agent.backtracking_algorithm(w):
                print("NIE UDAŁO SIĘ ZNALEŹĆ ŚCIEŻKI")
            else:
                track = agent.track[0] + agent.track[1]
                # iteration, Shortest track,robot track
                print(i, w.shortest_route, len(track))
                if anim:
                    anime = Anime(w, agent)
                    input()
        random_seed = random_seed + 1
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
