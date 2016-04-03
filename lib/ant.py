class Ant:

    def __init__(self, color, x, y):
        self.color = color
        self.coordinates = (x, y)
        self.lastSeveral == []

    def __str__(self):
        return '*'

    def get_possible_moves(self, lastSeveral):
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
            max_peromone_level = pheromones[point[0]][point[1]] if max_peromone_level < pheromones[point[0]][point[1]]

        Temp2 = []
        for point in Temp:
            Temp2.append(point) if pheromones[point[0]][point[1]] == max_peromone_level

        next = Temp2[rand(0, len(Temp2) - 1)]
        
        self.lastSeveral.append(next)
        if len(self.lastSeveral) > REMEBER_LAST_N: self.lastSeveral.pop(0)
        
        nx = next[0]
        ny = next[1]
        self.coordinates = (nx, ny)
        field[nx][ny] = "*"
