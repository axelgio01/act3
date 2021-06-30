"""

Pacman, classic arcade game.

"""

# Librerias que se van a estar usando
from random import choice
from turtle import *

from freegames import floor, vector

# Encontrar el maximo comun divisor de dos numeros
def gcd(a, b):
    return gcd(b, a % b) if b > 0 else a

# Encontrar el minimo comun multiplo
def lcm(a, b):
    return a / gcd(a, b) * b

# Contador de tiempo
elapsed = 0
# Velocidad (arbitraria) del Pacman
spdPacman = 100
# Velocidad (arbitraria) de los fantasmas
spdGhost = 80


ghostColors = ['red', 'green', 'orange', 'gray']

# Contiene la puntacion hasta el momento
state = {'score': 0}
# Turtle que estara dibujando a Pacman y a los fantasmas
path = Turtle(visible=False)
# Turtle que escribira mensajes en la pantalla
writer = Turtle(visible=False)
# Direccion en la que se estara moviendo el Pacman
aim = vector(5, 0)
# Posicion de Pacman
pacman = vector(-40, -80)
# Posiciones de los fantasmas con sus respectivas direcciones
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# Elemento que representa el tablero:
# 0 -> no se puede pasar por ahi
# 1 -> hay comida ahi
# 2 -> habia comida y ya fue recogida
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def getCoordinates(index):
    "Return coordinates x, y in turtle of a tile given the index"
    return (index % 20) * 20 - 200, 180 - (index // 20) * 20


def world():
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x, y = getCoordinates(index)
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    "Move pacman and all ghosts."
    global elapsed
    if elapsed % spdGhost == 0 or elapsed % spdPacman == 0:
        writer.undo()
        writer.write(state['score'])

        clear()

    if elapsed % spdPacman == 0:
        # Movimiento de Pacman
        # Revisar si la posicion esta disponible
        if valid(pacman + aim):
            pacman.move(aim)

        # Encontrar a Pacman en su nueva posicion
        index = offset(pacman)

        # Volver a dibujar el cuadro si es que Pacman se come el objeto
        if tiles[index] == 1:
            tiles[index] = 2
            state['score'] += 1
            x, y = getCoordinates(index)
            square(x, y)

    up()
    # Posicionar a Pacman en donde se va a dibujar
    goto(pacman.x + 10, pacman.y + 10)
    # Dibujar a Pacman
    dot(20, 'yellow')

    # Movimiento de los fantasmas
    # Declaracion de un fantasma
    it = 0
    for point, course in ghosts:
        if elapsed % spdGhost == 0:
            # Encontrar la diferencia de distancia del Pacman en "x" y "y"
            dx = point.x - pacman.x
            dy = point.y - pacman.y
            # Redefinir course si es que encuentra una posicion mas cercana
            if dy == 0:
                course = vector(5 if dx < 0 else -5, 0)
            elif dx == 0:
                course = vector(0, 5 if dy < 0 else -5)
            
            # Revisar si la posicion sugerida es valida
            if valid(point + course):
                point.move(course)
            # Si no lo es escoger aleatoriamente una de las dos sobrantes
            else:
                if course.x != 0:
                    op = [vector(0, -5), vector(0, 5)]
                    nextPos = choice(op)
                    course.x = nextPos.x
                    course.y = nextPos.y
                    if valid(point + course):
                        point.move(course)
                else:
                    op = [vector(5, 0), vector(-5, 0)]
                    nextPos = choice(op)
                    course.x = nextPos.x
                    course.y = nextPos.y
                    if valid(point + course):
                        point.move(course)

        up()
        # Posicionar al fantasma en donde se va a dibujar
        goto(point.x + 10, point.y + 10)
        # Dibujar al fantasma
        dot(20, ghostColors[it])
        it += 1

    if elapsed % spdGhost == 0 or elapsed % spdPacman == 0:
        update()

    # Revisar si hay colision entre pacman y un fantasma
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            # Detener el juego en caso de que choquen
            return

    elapsed += gcd(spdPacman, spdGhost)
    if elapsed == lcm(spdPacman, spdGhost):
        elapsed = 0
    ontimer(move, gcd(spdPacman, spdGhost))


def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()