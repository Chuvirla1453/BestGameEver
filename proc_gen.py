import random

from consts import *
from main import *

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
        self.turns = []

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

        self.r_width = r_height
        self.r_height = r_width

        r_map = [[] * r_width for _ in range(r_height)]
        for i in range(r_width):
            for j in range(r_height):
                r_map[i] += self.rooms[i + j]
        for i in range(len(r_map)):
            for j in range(10):
                t = []
                for p in r_map[i]:
                    t += p[j]

                self.my_map.append(t)

        for i in range(len(self.my_map)):
            for j in range(len(self.my_map[i])):
                if self.my_map[i][j] == '_':
                    t = Tile(i, j, 'floor')
                    self.floors.append(t)
                    self.my_map[i][j] = t
                elif self.my_map[i][j] == '#':
                    t = Tile(i, j, 'wall')
                    self.my_map[i][j] = t
                else:
                    t = Tile(i, j, 'none')
                    self.my_map[i][j] = t

        for j in range(4, len(self.my_map[0]), 10):  # Вертикальные коридоры
            w_count = 0
            cor_flag = False
            for i in range(len(self.my_map)):
                if self.my_map[i][j].type == 'wall':
                    w_count += 1
                    if w_count == self.r_height * 2:
                        break
                    if not w_count % 2:
                        cor_flag = True
                        #self.my_map[i + 1][j] = Tile(Tile(f, j * i, 'door')) Здесь можно дверь добавить, если понадобится
                    else:
                        cor_flag = False
                        if w_count > 1:
                            self.my_map[i][j + 1] = Tile(i, j + 1, 'floor')
                if cor_flag:
                    self.my_map[i][j] = Tile(i, j, 'wall')
                    self.my_map[i][j + 1] = Tile(i, j + 1, 'floor')
                    self.my_map[i][j + 2] = Tile(i, j + 2, 'wall')

        for i in range(4, len(self.my_map), 10):  # Горизонтальные коридоры
            w_count = 0
            cor_flag = False
            for j in range(len(self.my_map[i])):
                if self.my_map[i][j].type == 'wall':
                    w_count += 1
                    if w_count == self.r_width * 2:
                        break
                    if not w_count % 2:
                        cor_flag = True
                        #self.my_map[i + 1][j] = Tile(Tile(f, j * i, 'door')) Здесь можно дверь добавить, если понадобится
                    else:
                        cor_flag = False
                        if w_count > 1:
                            self.my_map[i + 1][j] = Tile(i + 1, j, 'floor')
                if cor_flag:
                    self.my_map[i][j] = Tile(i, j, 'wall')
                    self.my_map[i + 1][j] = Tile(i + 1, j, 'floor')
                    self.my_map[i + 2][j] = Tile(i + 2, j, 'wall')

    def place(self):
        empty_floors = self.floors.copy()
        hero_pos = random.randrange(len(self.floors))

        self.hero = MainCharacter(self.floors[hero_pos].get_pos()[0], self.floors[hero_pos].get_pos()[1], HERO_HP,
                                  "Hero", DAGGER, LEATHER, self)

        self.my_map[self.floors[hero_pos].get_pos()[0]][self.floors[hero_pos].get_pos()[1]].add_character(self.hero)

        del empty_floors[hero_pos]

        # print(*self.floors)
        # print(empty_floors[-1], empty_floors[-1].get_pos()[0], empty_floors[-5].get_pos()[1], self.my_map[empty_floors[-1].get_pos()[0]][empty_floors[-5].get_pos()[1]])
        # print(empty_floors[-1].get_pos() == self.my_map[empty_floors[-1].get_pos()[0]][empty_floors[-1].get_pos()[1]].get_pos())

        self.my_map[empty_floors[-5].get_pos()[0]][empty_floors[-5].get_pos()[1]] =\
            Tile(empty_floors[-5].get_pos()[0], empty_floors[-5].get_pos()[1], 'ladder')

        del empty_floors[-5]

        for _ in range(self.enemy_count):
            t = random.randrange(len(empty_floors))
            t1 = empty_floors[t]
            del empty_floors[t]
            enemy = random.choice(ENEMIES)
            if enemy == 'rat':
                e = BaseEnemy(t1.get_pos()[0], t1.get_pos()[1], RAT_SPRITE, RAT_HP, RAT_DAMAGE,
                              RAT_ARMOR, 'rat', self)
                self.turns.append(e)
                t1.add_character(e)

        stones = len(empty_floors) // 3
        for _ in range(stones):
            t = random.randrange(len(empty_floors))
            t1 = empty_floors[t]
            del empty_floors[t]
            t1.add_character(Stone())


if __name__ == '__main__':
    t = proc_gen(3).my_map
    for i in t:
        print(*i)



