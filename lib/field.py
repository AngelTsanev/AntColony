from settings import *
import time
from random import randint as rand


class Color:

    def __init__(self, red, green, blue):
        self.red   = red if 0 <= red < 256 else 0 if red < 0 else 255
        self.green = green if 0 <= green < 256 else 0 if green < 0 else 255
        self.blue  = blue if 0 <= blue < 256 else 0 if blue < 0 else 255

    def __getitem__(self, arg):
        if (arg == 'red' or arg == 0):
            return self.red 
        if (arg == 'green' or arg == 1):
            return self.green 
        if (arg == 'blue' or arg == 2):
            return self.blue
        raise IndexError


class Food:

    def __init__(self, color, x, y):
        self.color = color
        self.coordinates = (x, y)
        self.quanity = rand(50, 100)

    def eat(self):
        self.quanity -= 1

    def __str__(self):
        return '#'

    def move(self, field, pheromones):
        field[self.coordinates[0]][self.coordinates[1]] = "#"


class Ant:

    def __init__(self, color, x, y):
        self.color = color
        self.coordinates = (x, y)
        self.lastSeveral = []

    def __str__(self):
        return '*'

    def get_possible_moves(self, lastSeveral, field):
        x = self.coordinates[0]
        y = self.coordinates[1]
        Temp = []
        if (x + 1 < X and (x+1, y) not in lastSeveral and field[x+1][y] != "-"): Temp.append((x+1,y))
        if (x - 1 >= 0 and (x-1, y) not in lastSeveral and field[x-1][y] != "-"): Temp.append((x-1,y))
        if (y + 1 < Y and (x, y+1) not in lastSeveral and field[x][y+1] != "-"): Temp.append((x,y+1))
        if (y - 1 >= 0 and (x, y-1) not in lastSeveral and field[x][y-1] != "-"): Temp.append((x,y-1))
        return Temp

    def move(self, field, pheromones):
        x = self.coordinates[0]
        y = self.coordinates[1]
        field[x][y] = "-"
        #increase the pheromone level on (x, y)
        pheromones[x][y]+=1
        
        # find next field and remove from current field
        Temp = self.get_possible_moves(self.lastSeveral, field)
        #####
        #x--  this will bug in the drawn case, so if this happen we should empty the LastSeveralStack //FIXED
        #####
        if len(Temp) == 0:  
            Temp = self.get_possible_moves([], field)
            self.lastSeveral = []

        max_peromone_level = 0
        for point in Temp:
            if max_peromone_level < pheromones[point[0]][point[1]]: max_peromone_level = pheromones[point[0]][point[1]] 

        Temp2 = []
        for point in Temp:
            if pheromones[point[0]][point[1]] == max_peromone_level: Temp2.append(point)

        next = Temp2[rand(0, len(Temp2) - 1)]
        
        self.lastSeveral.append(next)
        if len(self.lastSeveral) > REMEBER_LAST_N: self.lastSeveral.pop(0)
        
        nx = next[0]
        ny = next[1]
        self.coordinates = (nx, ny)
        field[nx][ny] = "*"


class Field:

    def __init__(self, filename):
        self.units = []
        with open( filename , 'r') as file:
            self.canvas = [ line.split() for line in file]
        self.pheromones = [[0 for x in range(64)] for x in range(32)]

    def __str__(self):
        self.print()

    def generate_next(self):
        for unit in self.units:
            unit.move(self.canvas, self.pheromones)

    def print(self):
        for line in field.canvas:
            print(" ".join(line)) 
        print("")
        print("")
        print("")



field = Field("field.txt")
green = Color(0, 204, 0)
food = Food(green, 10, 10)
field.units.append(food)

for i in range(0 , 50):
    field.units.append(Ant(Color(0, 0, 100), 30, 30))

while True:
    field.print()
    field.generate_next()
    time.sleep(2)

