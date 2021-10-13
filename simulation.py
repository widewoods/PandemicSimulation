import random
from math import floor, sqrt
from time import sleep
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Person:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.infect_duration = 2
        self.travel_radius = 10
        self.infect_possibility = 0.3
        self.encounters_per_step = 6

        # S: Susceptible, I: Infected, R: Recovered
        self.status = "S"
        self.status_after_step = "S"
        self.infect_timer = 0

    # def get_neighbors(self, size):
    #     neighbors = []
    #     if self.x == 0:
    #         neighbors.append(population[self.x + 1][self.y])
    #     elif self.x == size - 1:
    #         neighbors.append(population[self.x - 1][self.y])
    #     else:
    #         neighbors.append(population[self.x + 1][self.y])
    #         neighbors.append(population[self.x - 1][self.y])
    #     if self.y == 0:
    #         neighbors.append(population[self.x][self.y + 1])
    #     elif self.y == size - 1:
    #         neighbors.append(population[self.x][self.y - 1])
    #     else:
    #         neighbors.append(population[self.x][self.y + 1])
    #         neighbors.append(population[self.x][self.y - 1])
    #
    #     return neighbors

    def get_people_in_radius(self, size):
        in_radius = []
        for i in range(self.x - self.travel_radius, self.x + self.travel_radius + 1):
            for j in range(self.y - self.travel_radius, self.y + self.travel_radius + 1):
                if (i >= 0) & (i < size):
                    if (j >= 0) & (j < size):
                        p = population[i][j]
                        distance = sqrt((self.x - p.x) * (self.x - p.x) + (self.y - p.y) * (self.y - p.y))
                        if (p != self) & (distance <= self.travel_radius):
                            in_radius.append(p)

        return in_radius

    def infect(self):
        in_radius = self.get_people_in_radius(grid_size)
        encounters = random.choices(in_radius, k=self.encounters_per_step)
        self.status_after_step = "I"
        for p in encounters:
            if (random.random() < self.infect_possibility) & (p.status == "S"):
                p.status_after_step = "I"

    def set_status(self, new_status):
        self.status = new_status


def timestep(pop):
    # timestep 전과 후를 따로 나누고 다 적용 후 덮어씌우기
    s_count = 0
    i_count = 0
    r_count = 0
    for i in range(0, grid_size):
        for p in pop[i]:
            if p.status == "I":
                p.infect()
                p.infect_timer += 1
                if p.infect_timer == p.infect_duration:
                    p.status_after_step = "R"

    for i in range(0, grid_size):
        for p in pop[i]:
            p.set_status(p.status_after_step)
            if p.status == "S":
                s_count += 1
            elif p.status == "I":
                i_count += 1
            else:
                r_count += 1

    SIR = (s_count, i_count, r_count)
    SIR_list[0] = np.append(SIR_list[0], np.array([SIR[0]]))
    SIR_list[1] = np.append(SIR_list[1], np.array([SIR[1]]))
    SIR_list[2] = np.append(SIR_list[2], np.array([SIR[2]]))

    return SIR


grid_size = 32
SIR_list = [np.array([grid_size * grid_size - 1]), np.array([1]), np.array([0])]
population = []
step_count = 1

for x in range(0, grid_size):
    population.append([])
    for y in range(0, grid_size):
        population[x].append(Person(x, y))

population[floor(grid_size/2)][floor(grid_size/2)].status = "I"

window = tk.Tk()
window.title("Simulation")
frames = []
for i in range(grid_size):
    frames.append([])
    for j in range(grid_size):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j)
        frm = tk.Frame(master=frame, width=round(600/grid_size), height=round(600/grid_size), bg="red")
        frm.pack()
        frames[i].append(frm)

while timestep(population)[1] != 0:
    for x in range(0, grid_size):
        for y in range(0, grid_size):
            if population[x][y].status == "I":
                frames[x][y].config(bg="red")
            elif population[x][y].status == "R":
                frames[x][y].config(bg="gray")
            else:
                frames[x][y].config(bg="white")
    window.update()
    step_count += 1

for x in range(0, grid_size):
    for y in range(0, grid_size):
        if population[x][y].status == "I":
            frames[x][y].config(bg="red")
        elif population[x][y].status == "R":
            frames[x][y].config(bg="gray")
        else:
            frames[x][y].config(bg="white")
    window.update()

x1 = np.arange(0, step_count + 1)

plt.bar(x1, height=SIR_list[0], bottom=SIR_list[1], color="c", label="Susceptible")
plt.bar(x1, height=SIR_list[1], color="r", label="Infected")
plt.bar(x1, height=SIR_list[2], bottom=SIR_list[0]+SIR_list[1], color="gray", label="Recovered")

plt.annotate("Infect Possibility: " + str(population[0][0].infect_possibility), xy=(0, -0.1), xycoords='axes fraction')
plt.annotate("Infect Duration: " + str(population[0][0].infect_duration), xy=(0, -0.134), xycoords='axes fraction')
plt.annotate("Travel Radius: " + str(population[0][0].travel_radius), xy=(0.6, -0.1),  xycoords='axes fraction')
plt.annotate("Encounters: " + str(population[0][0].encounters_per_step), xy=(0.6, -0.134), xycoords='axes fraction')

plt.legend(loc="upper right")
plt.xlabel("Time", fontsize=15)
plt.ylabel("Number of People")
plt.axis([0, step_count, 0, grid_size * grid_size])
plt.xticks(np.arange(1, step_count, step=5))
plt.title("SIR Model")

ax = plt.gca()
ax.set_facecolor('k')

plt.show()
