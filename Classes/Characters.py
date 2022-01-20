import pygame as pg

from Classes.Secondary_functions import load_image, load_music

HERO_SPRITE = load_image('Sprites', 'Animations', 'Hero', 'hero.png')
TILE_SIZE = (TILE_WIDTH, TILE_HEIGHT) = (64, 64)

"""_________SOME SOUNDS______________"""
RAT_ATTACK = load_music('Sounds', 'rat_attack.mp3')
RAT_DIE = load_music('Sounds', 'rat_die.mp3')
JUMP_SND = load_music('Sounds', 'jump.mp3')
RAT_POINTS = 5
"""___________________________________"""


class BaseCharacter(pg.sprite.Sprite):
    """Класс для основ всего 'живого'"""

    def __init__(self, x: int, y: int, image: pg.Surface, hp: int, name: str):
        """
        :params x, y: координата клетки к примеру (0, 1); (5, 4)
        :param image: путь к картинке
        :param hp: здровье
        :param name: имя персонажа
        """
        super().__init__()

        self.image = image
        self.rect = pg.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, *TILE_SIZE)

        self.cell = (x, y)

        self.name = name
        self.hp = hp

    def is_alive(self) -> bool:
        """Проверка, жив ли персонаж"""
        return self.hp > 0

    def move(self, dx: int, dy: int) -> None:
        """Передвинуть персонажа"""
        self.rect.x += dx * TILE_WIDTH
        self.rect.y += dy * TILE_HEIGHT
        self.cell = (self.cell[0] + dx, self.cell[1] + dy)

    def move_tile(self, dx: int, dy: int):
        self.rect.x -= dx * TILE_WIDTH
        self.rect.y -= dy * TILE_HEIGHT

    def get_damage(self, damage: int):
        """Ранение персонажа"""
        if self.is_alive():
            if damage > 0:
                self.hp -= damage

    def get_cell(self) -> (int, int):
        """Получение клетки, где сейчас находится герой"""
        return self.cell

    def get_coors(self) -> (int, int):
        """Получить координаты персонажа"""
        return self.rect.x, self.rect.y

    def set_pos(self, x: int, y: int) -> None:
        """Установить координаты персонажа"""
        self.rect.x, self.rect.y = x * TILE_WIDTH, y * TILE_HEIGHT


class MainCharacter(BaseCharacter):
    """
    Класс ГГ
    """

    def __init__(self, x: int, y: int, hp: int, name: str, weapon, armor, game_field):
        """
        :param weapon: оружие песронажа
        :param armor: броня персонажа
        :param game_field: игровое поле
        """
        self.image = HERO_SPRITE
        super().__init__(x, y, self.image, hp, name)

        self.rect = pg.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, *TILE_SIZE)

        self.cell = (x, y)

        self.weapon = weapon
        self.armor = armor
        self.name = name

        self.game_field = game_field
        self.inventory = [weapon, armor, []]

    def hit(self, target):
        target.get_damage(self.weapon.damage - target.armor)

    def change_weapon(self, new_weapon):
        del self.game_field.my_map[self.rect.y][self.rect.x].inventory[-1]
        if len(self.inventory[2]) < 6:  # Потом возможно поменяем вместимость
            self.inventory[2].append(self.weapon)
            self.weapon = new_weapon
            self.inventory[0] = new_weapon
        else:
            self.game_field.my_map[self.rect.y][self.rect.x].add_item(self.weapon)
            self.weapon = new_weapon
            self.inventory[0] = new_weapon

    def change_armor(self, new_armor):
        del self.game_field.my_map[self.rect.y][self.rect.x].inventory[-1]
        if len(self.inventory[2]) < 6:  # Потом возможно поменяем вместимость
            self.inventory[2].append(self.weapon)
            self.armor = new_armor
            self.inventory[1] = new_armor
        else:
            self.game_field.my_map[self.rect.y][self.rect.x].add_item(self.weapon)
            self.armor = new_armor
            self.inventory[1] = new_armor

    def move(self, dx: int, dy: int) -> None:
        self.cell = (self.cell[0] + dx, self.cell[1] + dy)


class BaseEnemy(BaseCharacter):
    """
    Здесь все враги
    """

    def __init__(self, x: int, y: int, image: pg.Surface, hp: int, damage: int, armor: int, name: str, game_field):
        super().__init__(x, y, image, hp, name)

        self.image = image
        self.rect = pg.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, *TILE_SIZE)
        self.cell = (x, y)

        self.game_field = game_field
        self.drop = None
        self.chance_of_drop = None
        self.damage = damage
        self.armor = armor

        if name == 'rat':
            self.death_snd = RAT_DIE
            self.attack_snd = RAT_ATTACK
            self.walk_snd = JUMP_SND
            self.points = RAT_POINTS

    def hit(self, target):
        target.get_damage(self.damage - target.armor.armor)


class Weapon:
    """Класс со значениями оружия"""

    def __init__(self, damage, sprite, name):
        self.damage = damage
        self.sprite = sprite
        self.name = name


class Armor:
    """Класс со значениями брони"""

    def __init__(self, armor, sprite, name):
        self.armor = armor
        self.sprite = sprite
        self.name = name
