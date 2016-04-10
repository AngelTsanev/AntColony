from settings import *
from random import randint as rand

class Ant:

    def __init__(self, color, x, y, number):
        self.color = color
        self.coordinates = (x, y)
        self.lastSeveral = [(x, y)]
        self.number = number
        self.freeze_n_steps = 0
        self.hasFood = False

    def __str__(self):
        return '*' #str(self.number)

    def get_possible_moves(self, lastSeveral, field, occupied):
        x = self.coordinates[0]
        y = self.coordinates[1]
        possible_moves = []
        if (x + 1 < X and (x+1, y) not in lastSeveral and (x+1, y) not in occupied): possible_moves.append((x+1,y))
        if (x - 1 >= 0 and (x-1, y) not in lastSeveral and (x-1, y) not in occupied): possible_moves.append((x-1,y))
        if (y + 1 < Y and (x, y+1) not in lastSeveral and (x, y+1) not in occupied): possible_moves.append((x,y+1))
        if (y - 1 >= 0 and (x, y-1) not in lastSeveral and (x, y-1) not in occupied): possible_moves.append((x,y-1))
        return possible_moves

    def base_in_range(self, moves, base):
        if base in moves:
            self.coordinates = (base[0], base[1])
            self.add_step_for_tracking(next)
            return True
        return False

    def food_in_range(self, moves, foods):
        reachable_food = []
        for move in moves:
            if move in foods:
                reachable_food.append(move)
        if len(reachable_food) == 0:
            return False
        else:
            next_step = reachable_food[rand(0, len(reachable_food) - 1)]
            self.coordinates = next_step
            self.add_step_for_tracking(next_step)
            return True

    def add_step_for_tracking(self, step):
        self.lastSeveral.append(step)
        if len(self.lastSeveral) > REMEBER_LAST_N: self.lastSeveral.pop(0)

    def move(self, field):
        if self.freeze_n_steps > 0:
            self.freeze_n_steps-=1
            if len(self.lastSeveral) > 1: self.lastSeveral.pop(0)
            #print("ANTONY " + str(self.number) + " has to sleep " + str(self.freeze_n_steps) + " more steps!")
            return
        canvas = field.canvas 
        pheromones = field.pheromones
        occupied = field.occupied

        x = self.coordinates[0]
        y = self.coordinates[1]
        canvas[x][y] = "0"
        field.remove_occupied((x,y))
        #print("ANTONY " + str(self.number) + " just left possition " + str(self.coordinates) + "!")
        #increase the pheromone level on (x, y)
        if self.hasFood:
            pheromones[x][y]+=7
        else:
            pheromones[x][y]+=2
        
        #find next step and remove from current field
        possible_moves = self.get_possible_moves(self.lastSeveral, canvas, occupied)
        #####
        #x--  this will bug in the drawn case, so if this happen we should empty the LastSeveralStack //FIXED
        #####
        if len(possible_moves) == 0:  
            #possible_moves = self.get_possible_moves([], canvas, occupied)
            #self.lastSeveral = []
            canvas[x][y] = self.__str__()
            self.freeze_n_steps = rand(0, 2)
            field.add_occupied(self.coordinates)
            #print("ANTONY " + str(self.number) + " just occupied possition " + str(self.coordinates) + " but he will sleep " + str(self.freeze_n_steps) + " steps!")
            return

        #if there is food in the ant's range and ant isn't carrying food... well we definately go on the food pixel
        #if ant is carrying food and the base is in range... well we go there to drop off the food
        if self.hasFood:
            if self.base_in_range(possible_moves, field.base): #returns true or false and if true sets new coordinates
                canvas[x][y] = self.__str__()
                #go in base and drop that food soldier!
                self.freeze_n_steps = rand(3, 8)
                self.hasFood = False
                field.add_occupied(self.coordinates)
                #print("ANTONY " + str(self.number) + " just occupied possition " + str(self.coordinates) + " but he will sleep " + str(self.freeze_n_steps) + " steps!")
                return
        else:
            if self.food_in_range(possible_moves, field.food): #returns true or false and if true sets new coordinates
                canvas[x][y] = self.__str__()
                self.freeze_n_steps = rand(1, 3)
                self.hasFood = True
                field.add_occupied(self.coordinates)
                #print("ANTONY " + str(self.number) + " just occupied possition " + str(self.coordinates) + " but he will sleep " + str(self.freeze_n_steps) + " steps!")
                return


        max_peromone_level = 0
        for point in possible_moves:
            if max_peromone_level < pheromones[point[0]][point[1]]: max_peromone_level = pheromones[point[0]][point[1]]

        better_moves = []
        for point in possible_moves:
            if pheromones[point[0]][point[1]] == max_peromone_level: better_moves.append(point)

        next = better_moves[rand(0, len(better_moves) - 1)]
        
        self.add_step_for_tracking(next)
        
        nx = next[0]
        ny = next[1]
        self.coordinates = (nx, ny)
        #print("ANTONY " + str(self.number) + " just occupied possition " + str(self.coordinates) + "!")
        field.add_occupied(self.coordinates)
        canvas[nx][ny] = self.__str__()
        return
