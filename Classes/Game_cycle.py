import pygame as pg
import sys

from Classes.Cells import *
from Classes.Characters import *
from Classes.Consts import *


def cycle():
    pass


def make_turn(field):
    while True:
        delta = ()
        action = False
        for i in pg.event.get():  # Проверяем действия игрока
            if i.type == pg.QUIT:
                sys.exit()
            elif i.type == pg.K_w or i.type == pg.K_UP:
                delta = (0, 1)
            elif i.type == pg.K_a or i.type == pg.K_LEFT:  # Дельта показывает на то, куда смещаются координаты (x, y)
                delta = (-1, 0)
            elif i.type == pg.K_s or i.typr == pg.K_DOWN:
                delta = (0, -1)
            elif i.type == pg.K_d or i.type == pg.K_RIGHT:
                delta = (0, 1)
            elif i.type == pg.K_e:
                action = True  # action - если игрок взаимодействует с клеткой, на которой стоит
        if delta:
            check_cell = (field.hero.get_cell()[0] + delta[0], field.hero.get_cell()[1] + delta[1])
            if field[check_cell[1]][check_cell[0]].type == 'floor':  # Если игрок наступает на пол
                if not field[check_cell[1]][check_cell[0]].character:
                    field.hero.move(delta[0], delta[1])
                    field[field.hero.get_cell()[1]][field.hero.get_cell()[0]].add_character(None)
                    field[check_cell[1]][check_cell[0]].add_character(field.hero)  # Если на полу ничего нет, то он идёт
                    # туда
                    WALK_SND.play()
                elif isinstance(field[check_cell[1]][check_cell[0]].character, Stone):
                    field[check_cell[1]][check_cell[0]].add_character(None)  # Если там камень, то он ломает его
                    BREAK_STONE_SND.play()
                elif isinstance(field[check_cell[1]][check_cell[0]].character, BaseEnemy):
                    field.hero.hit(field[check_cell[1]][check_cell[0]].character)  # Если враг, то бьёт его
                    HIT_SND.play()
            elif field[check_cell[1]][check_cell[0]].type == 'ladder':
                new_level()  # Если лестница, то идёт на следующий уровень
                LADDER_SND.play()
            else:
                WALK_IN_WALL_SND.play()  # Если стена, то пропускает свой ход, с помощью этого тупого действия
        if action:
            check_cell = field.hero.get_cell()
            if not field[check_cell[1]][check_cell[0]].has_item():  # Если ничего на полу нет, то тоже пропускает ход
                WALK_IN_WALL_SND.play()
            else:
                PICK_SND.play()  # Если что-то есть, то распределяется в инвентарь
                if isinstance(field[check_cell[1]][check_cell[0]].inventory[-1], Weapon):
                    field.hero.change_weapon(field[check_cell[1]][check_cell[0]].inventory[-1])
                elif isinstance(field[check_cell[1]][check_cell[0]].inventory[-1], Armor):
                    field.hero.change_armor(field[check_cell[1]][check_cell[0]].inventory[-1])


def new_level():  # В иделае здесь уровень генерировавть
    pass
