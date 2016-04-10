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

