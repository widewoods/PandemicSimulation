from random import random
import math


class Person:
    x = round(random() * 10, 2)
    y = round(random() * 10, 2)

    move_speed = 10
    is_infected = False
    remove_timer = 0
    is_removed = False

    def move(self):
        pass

    def get_people_in_radius(self):
        people_in_radius = []
        for i in range(len(population)):
            distance = math.sqrt((self.x - population[i].x) * (self.x - population[i].x) +
                                 (self.y - population[i].y) * (self.y - population[i].y))
            if distance < infectRadius:
                people_in_radius.append(population[i])
        return people_in_radius

    def infect(self, people_in_radius):
        for i in range(len(people_in_radius)):
            people_in_radius[i].is_infected = True


def timestep(pop):
    # timestep 전과 후를 따로 나누고 다 적용 후 덮어씌우기
    after_timestep = pop
    for i in range(len(pop)):
        if pop[i].is_infected:
            in_radius = pop[i].get_people_in_radius()
            after_timestep[i].remove_timer += 1
            after_timestep[i].infect(in_radius)
    return after_timestep


infectDuration = 3
infectRadius = 0.1
infectPossibility = 0.2

population = []

for j in range(0, 10):
    p = Person()
    population.append(p)

population[0].is_infected = True
population = timestep(population)
for j in range(len(population)):
    print(j, population[1].is_infected)

