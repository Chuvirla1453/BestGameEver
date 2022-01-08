import pygame as pg


from sys import exit
import os
from random import randint, choice

import proc_gen, consts

from AI import *

start_win_size = (start_win_width, start_win_height) = (600, 400)

start_win_btn_size = (start_win_btn_width, start_win_btn_height) = (140, 70)
start_win_btns_count = 3

# screen_size = (screen_width, screen_height) = (Tk().winfo_screenwidth(), Tk().winfo_screenheight())

tile_size = (tile_width, tile_height) = (64, 64)
tiles_sprites = pg.sprite.Group()


def load_image(*path):
    fullname = os.path.join('data', *path)
    # если файл не существует, то выходим
    if path[1] == 'none.png':
        image = pg.image.load(fullname)
    else:
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            exit()
        image = pg.image.load(fullname)
    return image


class Tile(pg.sprite.Sprite):
    """
    Класс с основными значениями тайлов
    """

    def __init__(self, x: int, y: int, image: str):  # x и y здесь - это на карте
        global tiles_sprites
        super(Tile, self).__init__()
        self.x, self.y = x, y
        self.type = image
        self.inventory = []
        self.character = None

        if image == 'wall':  # Я как обычно какую-то херню тут пишу, потом поправь, но типа так должно быть
            self.image = choice(consts.WALL_SPRITES)
        elif image == "floor":
            self.image = choice(consts.FLOOR_SPRITES)
        elif image == 'none':
            self.image = consts.NONE_SPRITE
        elif image == 'ladder':
            self.image = consts.LADDER_SPRITE
        self.rect = pg.Rect(x * tile_width, y * tile_height, *tile_size)
        tiles_sprites.add(self)
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
        return self.x, self.y

    def __str__(self):
        if self.type == 'wall':
            return '#'
        if self.type == 'floor':
            if type(self.character) == MainCharacter:
                return 'C'
            elif type(self.character) == Stone:
                return 's'
            elif type(self.character) == BaseEnemy:
                return 'R'
            return '_'
        if self.type == 'none':
            return '.'
        if self.type == 'ladder':
            return 'H'


class BaseCharacter(pg.sprite.Sprite):
    """
    Класс для основ всего 'живого'

    """

    def __init__(self, x: int, y: int, image: pg.Surface, hp: int, name: str):
        """
        :params x, y: координата клетки к примеру (0, 1); (5, 4)
        :param image: путь к картинке
        :param hp: здровье
        :param name: имя персонажа
        """
        super().__init__()

        self.rect = pg.Rect(x * tile_width, y * tile_height, *tile_size)
        self.cell = (x, y)

        self.name = name
        self.hp = hp

    def is_alive(self) -> bool:
        """
        Проверка, жив ли персонаж
        """
        return self.hp > 0

    def move(self, dx: int, dy: int) -> None:
        """
        Передвинуть персонажа
        """
        self.rect.x += dx
        self.rect.y += dy

    def get_damage(self, damage: int):
        """
        Ранение персонажа
        """
        if self.is_alive():
            if damage > 0:
                self.hp -= damage

    def get_cell(self) -> (int, int):
        """
        Получение клетки, где сейчас находится герой
        """
        return self.cell

    def get_coors(self) -> (int, int):
        """
        Получить координаты персонажа
        """
        return self.rect.x, self.rect.y

    def set_cell(self, x: int, y: int) -> None:
        """
        Установить клетку персонажа
        """
        self.cell = (x, y)
        self.rect.x, self.rect.y = x * tile_width, y * tile_height

    def set_coors(self, x: int, y: int) -> None:
        """
        Установить координаты персонажа
        """
        self.rect.x, self.rect.y = x, y
        self.cell = (x // self.rect.width, y // self.rect.height)


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
        self.image = consts.HERO_SPRITE
        super().__init__(x, y, self.image, hp, name)

        self.rect = pg.Rect(x * tile_width, y * tile_height, *tile_size)
        self.cell = (x, y)

        self.weapon = weapon
        self.armor = armor
        self.name = name

        self.game_field = game_field
        self.inventory = [weapon, armor, []]

    def hit(self, target):
        target.get_damage(self.weapon.damage - target.armor)

    def change_weapon(self, new_weapon):
        if len(self.inventory[2]) < 6:  # Потом возможно поменяем вместимость
            self.inventory[2].append(self.weapon)
            self.weapon = new_weapon
            self.inventory[0] = new_weapon
        else:
            self.game_field.search_tile(self.rect.x, self.rect.y).add_item(self.weapon)
            self.weapon = new_weapon
            self.inventory[0] = new_weapon


class BaseEnemy(BaseCharacter):
    """
    Здесь все враги
    """

    def __init__(self, x: int, y: int, image: pg.Surface, hp: int, damage: int, armor: int, name: str, game_field):
        super().__init__(x, y, image, hp, name)

        self.image = image
        self.rect = pg.Rect(x * tile_width, y * tile_height, *tile_size)
        self.cell = (x, y)

        self.game_field = game_field
        self.drop = None
        self.chance_of_drop = None
        self.damage = damage
        self.armor = armor

    def hit(self, target):
        target.get_damage(self.damage)


class Weapon:
    """
    Класс со значениями оружия
    """

    def __init__(self, damage, sprite, name):
        self.damage = damage
        self.sprite = sprite
        self.name = name


class Armor:
    """
    Класс со значениями брони
    """

    def __init__(self, armor, sprite, name):
        self.armor = armor
        self.sprite = sprite
        self.name = name


class Stone:
    pass


class Text(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, text: str, font_size: int, text_color=(255, 0, 0), back_color=(255, 255, 255)):
        super().__init__()
        self.text_color, self.back_color = text_color, back_color

        font = pg.font.SysFont('Times New Roman', font_size)
        self.text = font.render(text, True, text_color)

        self.image = pg.Surface((self.text.get_width() + 20, self.text.get_height() + 20))

        self.rect = pg.Rect(x, y, *self.image.get_size())
        self.extreme_points = [(0, 0), (self.rect.width, 0), (self.rect.width, self.rect.height), (0, self.rect.height)]

        self.update()

    def update(self) -> None:
        self.image.fill(self.back_color)
        self.image.blit(self.text, ((self.image.get_width() - self.text.get_width()) // 2,
                                    (self.image.get_height() - self.text.get_height()) // 2))

        for i in range(len(self.extreme_points)):
            pg.draw.line(self.image, self.text_color, self.extreme_points[i],
                         self.extreme_points[(i + 1) % len(self.extreme_points)], width=5)


class Button(pg.sprite.Sprite):
    """
    Класс кнопки, для удобной работы в меню
    """

    def __init__(self, ind: int, x: int, y: int, width_: int, height_: int, text: str, text_font: int,
                 text_color=(255, 255, 255), back_color=(0, 0, 0)):
        super().__init__()
        self.index = ind
        self.text_color = text_color
        self.back_color = back_color

        font = pg.font.SysFont('Times New Roman', text_font)
        self.text = font.render(text, True, text_color)

        self.image = pg.Surface((width_, height_))

        self.rect = pg.Rect(x, y, width_, height_)
        self.extreme_points = [(0, 0), (self.rect.width, 0), (self.rect.width, self.rect.height), (0, self.rect.height)]

        self.update()

    def update(self) -> None:
        """
        Отрисовка текста и узора кнопки
        """
        self.image.fill(self.back_color)
        self.image.blit(self.text, (self.rect.width // 2 - self.text.get_width() // 2,
                                    self.rect.height // 2 - self.text.get_height() // 2))

        for i in range(len(self.extreme_points)):
            pg.draw.line(self.image, self.text_color, self.extreme_points[i],
                         self.extreme_points[(i + 1) % len(self.extreme_points)], width=5)

    def crossed(self, x: int, y: int) -> bool:
        """
        Проверка, назодится ди координата в диапозоне координат кнопки
        """
        return self.rect.collidepoint(x, y)


def set_start_win_btns(y: int, win_width: int, btn_width: int, btn_height: int, btn_count: int,
                       text_color: (int, int, int), back_color: (int, int, int)) -> pg.sprite.Group:
    """
    Генерация заданного количесва кнопок с опреденным шаблном
    """
    dist_btns = (win_width - btn_width * btn_count) // (btn_count + 1)
    btns_sprites_ = pg.sprite.Group([Button(x, x * (btn_width + dist_btns) + dist_btns, y, btn_width, btn_height,
                                            f'{x + 1} уровень', 30, text_color, back_color) for x in range(btn_count)])
    return btns_sprites_


def align(display_length: int, sprite_length: int) -> int:
    """
    Возвращает коррдинату для выравнивания объекта по середине
    """
    return (display_length - sprite_length) // 2


def terminate() -> None:
    pg.quit()
    exit()


if __name__ == '__main__':
    fps = 60

    pg.init()

    window = 0
    screen = pg.display.set_mode(start_win_size)
    pg.display.set_caption('Стартовое окно')

    start_btns_sprites = set_start_win_btns(300, start_win_width, start_win_btn_width, start_win_btn_height,
                                            start_win_btns_count, (0, 255, 0), (0, 0, 0))

    game_title = Text(40, 40, 'The Best Game Ever', 30, (0, 255, 0), (0, 0, 0))
    game_title.rect.x = align(screen.get_width(), game_title.rect.w)
    text_sprites = pg.sprite.Group([game_title])

    game_field = None
    enemies_sprites = pg.sprite.Group()
    main_hero_sprites = pg.sprite.Group()

    while True:
        if window == 0:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for btn in start_btns_sprites:
                            if btn.crossed(*event.pos):  # Здесь должна происходить загрузка уровня
                                print(f'Запускается {btn.index + 1} уровень')
                                window = 1

                                game_field = proc_gen.proc_gen(1).my_map
                                # for y, row in enumerate(game_field):
                                #     for x, cell in enumerate(row):
                                #         if cell == '#':
                                #             tiles_sprites.add(
                                #                 Tile(x, y, load_image('Sprites', 'Wall', f'{randint(1, 4)}.png')))
                                #         if cell == '_':
                                #             tiles_sprites.add(
                                #                 Tile(x, y, load_image('Sprites', 'Floor', f'{randint(1, 5)}.png')))

                                screen = pg.display.set_mode(flags=pg.FULLSCREEN)
                                break

            text_sprites.draw(screen)
            start_btns_sprites.draw(screen)

        elif window == 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()

            tiles_sprites.draw(screen)
            enemies_sprites.draw(screen)
            main_hero_sprites.draw(screen)

        pg.display.flip()
        screen.fill((0, 0, 0))
