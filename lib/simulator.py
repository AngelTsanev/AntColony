from rgbmatrix import RGBMatrix
from rgbmatrix import graphics
from field import Field
from color import Color
from ant import Ant
import time


Matrix = RGBMatrix(32, 2, 1)
Matrix.pwmBits = 5
Matrix.brightness = 100

def colorize(foods, base, ants):
    for food in foods:
        Matrix.SetPixel(food[1], food[0], 0, 200, 0)
    for ant in ants:
        Matrix.SetPixel(ant.coordinates[1], ant.coordinates[0], 200, 0, 0)
	#base
    Matrix.SetPixel(base[1], base[0], 100, 255, 100)


field = Field("field.txt", (30, 40))

field.food.append((10, 10))
field.food.append((20, 20))

for i in range(1, 21):
    field.units.append(Ant(Color(0, 0, 100), 30, 40, i))
    field.add_occupied((30, 40))

offscreenCanvas = Matrix.CreateFrameCanvas()

i = 1
while True:
    i+=1
    offscreenCanvas.Clear()
    field.draw()
    field.generate_next()
    colorize(field.food, field.base, field.units)
    if i % 10 == 0:
        i = 1
        field.evaporate_pheromones()
    time.sleep(1)
    offscreenCanvas = Matrix.SwapOnVSync(offscreenCanvas)

