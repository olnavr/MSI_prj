#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wourld import Wourld
from room import Room
from anime import Anime
from agent import Agent

def main(args):
    r_list = [[12, 11, 5, 3], [17, 7, 5, 3]]
    w = Wourld(r_list, 3)
    w.combine2Rooms()
    w.calcTargets()
    agent = Agent(w.agent_sp, w.targets)
    agent.backtracking_algorithm(w)
    agent.backtracking_algorithm(w)
    track = agent.track[0] + agent.track[1]
    for t in track:
        print(t)
    anime = Anime(w, agent)
    input()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
