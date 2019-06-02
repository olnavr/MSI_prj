import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.animation as animation
from wourld import Wourld

class Anime:
    def __init__(self, wourld, agent):
        self.canvas_size = wourld.canvas_size
        self.agent = agent
        self.htime = 0
        self.hlen = len(agent.track[0]) + len(agent.track[1])
        self.agent_track = agent.track[0] + agent.track[1]
        self.rooms = wourld.rooms
        self.doors = wourld.doors
        self.update = wourld.update
        self.fg = plt.figure()
        self.ani = animation.FuncAnimation(self.fg, self.animate_from_history, 360)
        self.fg.show()
        for i in range(self.hlen):
            self.update()

    def configurePlt(self):
        axes = self.fg.gca()
        xmajor_ticks = np.arange(0, self.canvas_size[0] + 1, 1)
        ymajor_ticks = np.arange(0, self.canvas_size[1] + 1, 1)
        axes.set_xticks(xmajor_ticks)
        axes.set_yticks(ymajor_ticks)
        axes.grid(which='major', alpha=0.2)
        axes.set_xlim([-1, self.canvas_size[0] + 1])
        axes.set_ylim([-1, self.canvas_size[1] + 1])
        axes.grid(True)

    def animate_from_history(self, e):
        axes = self.fg.gca()
        axes.cla()
        self.configurePlt()
        for r in self.rooms[:]:
            l = r.anti_origin[0] - r.origin[0]
            w = r.anti_origin[1] - r.origin[1]
            axes.add_patch(Rectangle(r.origin, l, w, alpha=1, linewidth=2.2, facecolor='lavender', edgecolor='red'))
        for d in self.doors:
            axes.plot(d.x, d.y, 'y-', linewidth=4)
            axes.plot(d.x[0], d.y[0], 'y*', linewidth=4)
        for r in self.rooms:
            for o in r.obstacles_c:
                axes.plot(o.cells[0] + 0.5, o.cells[1] + 0.5, "r*", linewidth=6)
        for r in self.rooms:
            for o in r.obstacles_mov:
                axes.plot(o.history[self.htime][0] + 0.5, o.history[self.htime][1] + 0.5, "m*", linewidth=6)
        axes.plot(self.agent_track[self.htime][0] + 0.5, self.agent_track[self.htime][1] + 0.5, marker="D", color="g", linewidth=6)
        self.htime = (self.htime + 1) % self.hlen
