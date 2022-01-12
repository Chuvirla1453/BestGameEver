import pygame as pg
from random import choice

from Classes.Characters import BaseEnemy, MainCharacter
from Classes.Consts import (LADDER_SPRITE, NONE_SPRITE, FLOOR_SPRITES, STONE_SPRITE,
                            WALL_SPRITES, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT)


class Tile(pg.sprite.Sprite):
    """Класс с основными значениями тайлов"""

    def __init__(self, x: int, y: int, image: str):  # x и y здесь - это на карте
        super(Tile, self).__init__()
        self.type = image
        self.inventory = []
        self.character = None

        if image == 'wall':  # Я как обычно какую-то херню тут пишу, потом поправь, но типа так должно быть
            self.image = choice(WALL_SPRITES)
        elif image == "floor":
            self.image = choice(FLOOR_SPRITES)
        elif image == 'none':
            self.image = NONE_SPRITE
        elif image == 'ladder':
            self.image = LADDER_SPRITE
        elif image == 'stone':
            self.image = choice(STONE_SPRITE)
        self.rect = pg.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, *TILE_SIZE)
        self.cell = (x, y)

    def render_lying_object(self):
        """
        if self.tile_inventory[-1] == ...  Здесь будем смотреть спрайт для последнего
        лежащего предмета и рендерить его
        """
        pass

    def add_items(self, item):
        self.inventory.append(item)

    def add_character(self, character):
        self.character = character

    def has_item(self):
        return bool(len(self.inventory))

    def has_character(self):
        return bool(self.character)

    def get_pos(self):
        return self.cell

    def set_pos(self, x_: int, y_: int):
        self.rect = pg.Rect(x_ * TILE_WIDTH, y_ * TILE_HEIGHT, *TILE_SIZE)
        self.cell = (x_, y_)

    def __str__(self):
        if self.type == 'wall':  # стенка
            return '#'
        if self.type == 'floor':  # пол
            #  if type(self.character) == MainCharacter:
            if isinstance(self.character, MainCharacter):  # главный герой
                return 'C'
            #   elif type(self.character) == Stone:
            elif isinstance(self.character, Stone):  # камень
                return 's'
            #  elif type(self.character) == BaseEnemy:
            elif isinstance(self.character, BaseEnemy):  # враг (крыса)
                return 'R'
            return '_'
        if self.type == 'none':  # пустота
            return '.'
        if self.type == 'ladder':  # лесница
            return 'H'


class Stone(pg.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()

        self.image = choice(STONE_SPRITE)
        self.rect = pg.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, *TILE_SIZE)

    def set_pos(self, x: int, y: int):
        self.rect.x, self.rect.y = x * TILE_WIDTH, y * TILE_HEIGHT
