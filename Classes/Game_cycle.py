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
        for i in pg.event.get():
            if i.type == pg.QUIT:
                sys.exit()
            elif i.type == pg.K_w or i.type == pg.K_UP:
                delta = (0, 1)
            elif i.type == pg.K_a or i.type == pg.K_LEFT:
                delta = (-1, 0)
            elif i.type == pg.K_s or i.typr == pg.K_DOWN:
                delta = (0, -1)
            elif i.type == pg.K_d or i.type == pg.K_RIGHT:
                delta = (0, 1)
            elif i.type == pg.K_e:
                action = True
        if delta:
            check_cell = (field.hero.get_cell()[0] + delta[0], field.hero.get_cell()[1] + delta[1])
            if field[check_cell[1]][check_cell[0]].type == 'floor':
                if not field[check_cell[1]][check_cell[0]].character:
                    field.hero.move(delta[0], delta[1])
                    field[field.hero.get_cell()[1]][field.hero.get_cell()[0]].add_character(None)
                    field[check_cell[1]][check_cell[0]].add_character(field.hero)
                    WALK_SND.play()
                elif isinstance(field[check_cell[1]][check_cell[0]].character, Stone):
                    field[check_cell[1]][check_cell[0]].add_character(None)
                    BREAK_STONE_SND.play()
                elif isinstance(field[check_cell[1]][check_cell[0]].character, BaseEnemy):
                    field.hero.hit(field[check_cell[1]][check_cell[0]].character)
            elif field[check_cell[1]][check_cell[0]].type == 'ladder':
                new_level()
                LADDER_SND.play()
            else:
                WALK_IN_WALL_SND.play()
        if action:
            check_cell = field.hero.get_cell()
            if not field[check_cell[1]][check_cell[0]].has_item():
                WALK_IN_WALL_SND.play()
            else:
                PICK_SND.play()
                if isinstance(field[check_cell[1]][check_cell[0]].inventory[-1], Weapon):
                    field.hero.change_weapon(field[check_cell[1]][check_cell[0]].inventory[-1])
                elif isinstance(field[check_cell[1]][check_cell[0]].inventory[-1], Armor):
                    field.hero.change_armor(field[check_cell[1]][check_cell[0]].inventory[-1])


def new_level():
    pass
