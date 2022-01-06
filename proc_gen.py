import random
from main import *
from consts import *
import math


def proc_gen(level):
    return Map(level)


class Map:
    def __init__(self, level):
        self.enemy_count = 5 * level + random.randint(-1, 3 * level)
        self.room_count = 3 * level + random.randint(-1, 2 * level)
        self.width = int(self.room_count ** 0.5 * 10)
        self.height = int(self.room_count ** 0.5 * 10)
        self.my_map = []
        self.rooms = []
        self.floors = []

        for i in range(self.room_count):
            self.create_room()

        self.create_map()
        self.place()

    def create_room(self):
        height = random.randint(4, 10)
        width = random.randint(4, 10)
        room = [['.'] * 10 for _ in range(10)]
        for i in range(10):
            for j in range(10):
                f = i in range(5 - (height // 2), 9 - (5 - (height // 2)) + 1) and\
                        j in range(5 - (width // 2), 9 - (5 - (width // 2)) + 1)

                if (i == 5 - (height // 2) or i == 9 - (5 - (height // 2)) or j == 5 - (width // 2)\
                        or j == 9 - (5 - (width // 2))) and f:
                    room[i][j] = '#'
                elif f:
                    room[i][j] = '_'

        self.rooms.append(room)

    def create_map(self):
        r_height = math.ceil(self.room_count ** 0.5)
        r_width = math.ceil(self.room_count / r_height)
        r_map = [[] * r_width for _ in range(r_height)]
        for i in range(r_width):
            for j in range(r_height):
                r_map[i] += self.rooms[i + j]
        for i in r_map:
            print(r_width, r_height)
            for j in i:
                print(j)
        for i in range(len(r_map)):
            for j in range(10):
                t = []
                for p in r_map[i]:
                    t += p[j]
                for f in range(len(t)):
                    if t[f] == '_':
                        tf = Tile(f, j * i, 'floor')
                        self.floors.append(tf)
                        t[f] = tf
                    elif t[f] == '#':
                        tf = Tile(f, j * i, 'wall')
                        t[f] = tf

        # Вот тута будут коридоры делаться, но мне лень
                self.my_map.append(t)

    def place(self):
        hero_pos = random.randrange(len(self.floors))
        self.hero = MainCharacter(self.floors[hero_pos].get_pos()[0], self.floors[hero_pos].get_pos()[1], HERO_HP,
                                  "Hero", DAGGER, LEATHER, self)

        for i in range(self.enemy_count):
            pass # НУЖНО: дописать коридоры, привязать героя на тайл, заспавнить сундуки, врагов, вписать их в очередь

if __name__ == '__main__':
    t = proc_gen(1).my_map
    for i in t:
        print(*i)



