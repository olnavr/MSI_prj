import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
from wourld import Wourld

class Anime:
    def __init__(self, wourld, agent, type):
        self.canvas_size = wourld.canvas_size
        self.agent = agent
        self.htime = 0 # aktualna chwila czasowa
        self.hlen = len(agent.track[0]) + len(agent.track[1]) #dłogość historii
        self.agent_track = agent.track[0] + agent.track[1] # ścieżka robota
        self.rooms = wourld.rooms
        self.doors = wourld.doors
        self.update = wourld.update
        self.fg = plt.figure()

        for i in range(self.hlen):
            self.update() # tworzenie historii
        if type == 'c': # tworzenie ciągłej animaji w okienku
            self.ani = animation.FuncAnimation(self.fg, self.animate_from_history, 360)
            self.fg.show() 
        elif type == 'm': # tworzenie filmików
            self.ani = animation.FuncAnimation(self.fg, self.animate_from_history, 360, save_count=self.hlen)
            self.animate_movie(1)


	# konfiguracja wyświetlanego obrazu, doposowanie wymiarów do światu
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
		
	# Tworzenie śwaitu w kroku h
    def animate_from_history(self, e):
        axes = self.fg.gca()
        axes.cla()
        self.configurePlt()
        for r in self.rooms[:]: #rysowanie pokojów
            l = r.anti_origin[0] - r.origin[0]
            w = r.anti_origin[1] - r.origin[1]
            axes.add_patch(Rectangle(r.origin, l, w, alpha=1, linewidth=2.2, facecolor='lavender', edgecolor='red'))
        for d in self.doors:# rysowanie dzwi
            axes.plot(d.x, d.y, 'y-', linewidth=4)
            axes.plot(d.x[0], d.y[0], 'y*', linewidth=4)
        for r in self.rooms: # rysowanie przeszkod nieruchomych
            for o in r.obstacles_c:
                axes.plot(o.cells[0] + 0.5, o.cells[1] + 0.5, "r*", linewidth=6)
        for r in self.rooms: # rysowanie prszeszkód ruchomych
            for o in r.obstacles_mov:
                axes.plot(o.history[self.htime][0] + 0.5, o.history[self.htime][1] + 0.5, "m*", linewidth=6)
        axes.plot(self.agent_track[self.htime][0] + 0.5, self.agent_track[self.htime][1] + 0.5, marker="D", color="g", linewidth=6)
        self.htime = (self.htime + 1) % self.hlen
        return axes


    def animate_movie(self, e): # zapis filmika
        print('probe1')
        ffwriter = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
        self.ani.save('basic_animation.mp4', writer=ffwriter)
        print('probe2')



