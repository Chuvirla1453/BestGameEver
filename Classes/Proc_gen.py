import random
import math

from Classes.Cells import *
from Classes.Characters import BaseEnemy, MainCharacter
from Classes.Consts import HERO_HP, RAT_HP, RAT_DAMAGE, RAT_ARMOR, RAT_SPRITE, DAGGER, LEATHER, ENEMIES


def proc_gen(level):
    return Map(level)


class Map:
    def __init__(self, level):
        self.enemy_count = 15 * level + random.randint(-1, 3 * level)
        self.room_count = (level * 2) ** 2
        #self.enemy_count = 1
        #self.room_count = 1
        self.width = int(self.room_count ** 0.5 * 10)
        self.height = int(self.room_count ** 0.5 * 10)
        self.my_map = []
        self.rooms = []
        self.floors = []
        self.turns = []

        self.r_width = 0
        self.r_height = 0
        self.hero = None

        for ifg in range(self.room_count):
            self.create_room()

        self.create_map()
        self.place()

    def create_room(self):
        height = random.randint(4, 10)
        width = random.randint(4, 10)
        room = [['.'] * 10 for _ in range(10)]
        for ikl in range(10):
            for j in range(10):
                f = ikl in range(5 - (height // 2), 9 - (5 - (height // 2)) + 1) and \
                    j in range(5 - (width // 2), 9 - (5 - (width // 2)) + 1)

                if (ikl == 5 - (height // 2) or ikl == 9 - (5 - (height // 2)) or j == 5 - (width // 2) or
                    j == 9 - (5 - (width // 2))) and f:
                    room[ikl][j] = '#'
                elif f:
                    room[ikl][j] = '_'

        self.rooms.append(room)

    def create_map(self):
        r_height = math.ceil(self.room_count ** 0.5)
        r_width = math.ceil(self.room_count / r_height)

        self.r_width = r_height
        self.r_height = r_width

        r_map = [[] * r_width for _ in range(r_height)]
        for iuio in range(r_width):
            for j in range(r_height):
                if self.room_count <= iuio * r_height + j:
                    r_map[iuio] += [['.'] * 10 for _ in range(10)]
                else:
                    r_map[iuio] += self.rooms[iuio * r_height + j]
        for iuio in range(len(r_map)):
            for j in range(10):
                t1 = []
                for p in r_map[iuio]:
                    t1 += p[j]

                self.my_map.append(t1)

        for iuio in range(len(self.my_map)):
            for j in range(len(self.my_map[iuio])):
                if self.my_map[iuio][j] == '_':
                    t1 = Tile(j, iuio, 'floor')
                    self.floors.append(t1)
                    self.my_map[iuio][j] = t1
                elif self.my_map[iuio][j] == '#':
                    t1 = Tile(j, iuio, 'wall')
                    self.my_map[iuio][j] = t1
                else:
                    t1 = Tile(j, iuio, 'none')
                    self.my_map[iuio][j] = t1

        for j in range(4, len(self.my_map[0]), 10):  # ???????????????????????? ????????????????
            w_count = 0
            cor_flag = False
            for iuio in range(len(self.my_map)):
                if self.my_map[iuio][j].type == 'wall':
                    w_count += 1
                    if w_count == self.r_height * 2:
                        break
                    if not w_count % 2:
                        cor_flag = True
                        #  self.my_map[iuio + 1][j] = Tile(Tile(f, j * iuio, 'door')) ?????????? ?????????? ?????????? ????????????????,
                        #  ???????? ??????????????????????
                    else:
                        cor_flag = False
                        if w_count > 1:
                            self.my_map[iuio][j + 1] = Tile(j + 1, iuio, 'floor')
                if cor_flag:
                    self.my_map[iuio][j] = Tile(j, iuio, 'wall')
                    self.my_map[iuio][j + 1] = Tile(j + 1, iuio, 'floor')
                    self.my_map[iuio][j + 2] = Tile(j + 2, iuio, 'wall')

        for iuio in range(4, len(self.my_map), 10):  # ???????????????????????????? ????????????????
            w_count = 0
            cor_flag = False
            for j in range(len(self.my_map[iuio])):
                if self.my_map[iuio][j].type == 'wall':
                    w_count += 1
                    if w_count == self.r_width * 2:
                        break
                    if not w_count % 2:
                        cor_flag = True
                        #  self.my_map[iuio + 1][j] = Tile(Tile(f, j * iuio, 'door')) ?????????? ?????????? ?????????? ????????????????, ????????
                        #  ??????????????????????
                    else:
                        cor_flag = False
                        if w_count > 1:
                            self.my_map[iuio + 1][j] = Tile(j, iuio + 1, 'floor')
                if cor_flag:
                    self.my_map[iuio][j] = Tile(j, iuio, 'wall')
                    self.my_map[iuio + 1][j] = Tile(j, iuio + 1, 'floor')
                    self.my_map[iuio + 2][j] = Tile(j, iuio + 2, 'wall')

    def place(self):
        empty_floors = self.floors.copy()
        hero_pos = random.randrange(len(self.floors))

        self.hero = MainCharacter(self.floors[hero_pos].get_pos()[0], self.floors[hero_pos].get_pos()[1], HERO_HP,
                                  "Hero", DAGGER, LEATHER, self)

        self.my_map[self.floors[hero_pos].get_pos()[1]][self.floors[hero_pos].get_pos()[0]].add_character(self.hero)

        del empty_floors[hero_pos]

        self.my_map[empty_floors[-5].get_pos()[1]][empty_floors[-5].get_pos()[0]] =\
            Tile(empty_floors[-5].get_pos()[0], empty_floors[-5].get_pos()[1], 'ladder')

        del empty_floors[-5]
        for _ in range(self.enemy_count):
            tg = random.randrange(len(empty_floors))
            t1 = empty_floors[tg]
            del empty_floors[tg]
            enemy = random.choice(ENEMIES)
            if enemy == 'rat':
                e = BaseEnemy(t1.get_pos()[0], t1.get_pos()[1], RAT_SPRITE, RAT_HP, RAT_DAMAGE,
                              RAT_ARMOR, 'rat', self)
                self.turns.append(e)
                t1.add_character(e)

        stones = len(empty_floors) // 3
        for _ in range(stones):
            tg = random.randrange(len(empty_floors))
            t1 = empty_floors[tg]
            del empty_floors[tg]
            t1.add_character(Stone(t1.get_pos()[0], t1.get_pos()[1]))


if __name__ == '__main__':
    t = proc_gen(3).my_map
    for i in t:
        print(*i)
