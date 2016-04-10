from settings import *
import time
from random import randint as rand
from ant import Ant
from color import Color

class Field:

    def __init__(self, filename, base_coordinates):
        self.units = []
        self.food = []
        self.base = base_coordinates

        with open( filename , 'r') as file:
            self.canvas = [line.split() for line in file]
        self.pheromones = [[0 for x in range(64)] for x in range(32)]
        self.occupied = []

    def __str__(self):
        self.print()

    def generate_next(self):
        #must evaporate some pheromones at some point
        #draw all the food // this way ants will be visible over the food
        for food in self.food:
            x = food[0]
            y = food[1]
            self.canvas[x][y] = "#"

        for unit in self.units:
            unit.move(self)

        #draw the base //this way base will be visible over the ants !
        x = self.base[0]
        y = self.base[1]
        self.canvas[x][y] = 'X'

    def print(self):
        for line in field.canvas:
            print(" ".join(line)) 
        print("")
        print("")
        print("")

    def evaporate_pheromones(self):
        for x in range(32):
            for y in range(64):
                if self.pheromones[x][y] > 0:
                    self.pheromones[x][y] -= 1

    def add_occupied(self, spot):
        self.occupied.append(spot)

    def remove_occupied(self, spot):
        index = self.occupied.index(spot)
        self.occupied.pop(index)



field = Field("field.txt", (30, 40))
#green = Color(0, 204, 0)
#food = Food(green, 10, 10)
field.food.append((10, 10))
field.food.append((20, 20))

for i in range(1, 30):
    field.units.append(Ant(Color(0, 0, 100), 30, 40, i))
    field.add_occupied((30, 40))

i = 1
while True:
    i+=1
    field.print()
    field.generate_next()
    if i % 10 == 0:
        i = 1
        field.evaporate_pheromones()
    time.sleep(0.4)


