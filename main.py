import pygame as pg
from sys import exit
from proc_gen import *
from AI import *


start_win_size = (start_win_width, start_win_height) = (600, 400)

start_win_btn_size = (start_win_btn_width, start_win_btn_height) = (140, 70)
start_win_btns_count = 3

class GameField:
    """
    Класс с основной игровой логикой, ходами, картой с врагами и.т.д.
    """
    def __init__(self, level):
        self.map = proc_gen(level)
        width, height = 1488, 420 # Потом переделаем
        self.camera = Camera(self.map.hero, self.map, width, height)
        self.turns = self.map.turns
        self.turn = 0

    def render(self): # Тут проигрываем все анимации и обновляем камеру
        self.camera.update()

    def check_activity(self): # Тут обновляем значения
        pass

    def turn_system(self):
        if self.turn == 0:
            pass # Выбирает игрок свой ход
        else:
            calculate_turn(self.map.get_character(self.turn))

        self.check_activity()

    def search_tile(self, x, y):
        return self.map.cells[y][x]


class Tile:
    """
    Класс с основными значениями тайлов
    """
    def __init__(self, x, y, type_of_cell): # x и y здесь - это на карте
        self.x = x
        self.y = y
        self.type_of_cell = type_of_cell
        self.collision = False
        self.enemy_collision = False
        self.end = False
        self.tile_inventory = []
        if self.type_of_cell == 'wall':
            self.collision = True
            self.sprite = 'wall.png'
        elif self.type_of_cell == 'door':
            self.enemy_collision = True
            self.sprite = 'door.png'
        elif self.type_of_cell == 'ladder':
            self.end = True
            self.sprite = 'ladder.png'
        else:
            self.sprite = 'floor.png'

    def render_lying_odject(self):
        pass
        # if self.tile_inventory[-1] == ...  Здесь будем смотреть спрайт для последнего
        # лежащего предмета и рендерить его

    def add_item(self, item):
        self.tile_inventory.append(item)


class Camera: # x и y здесь - это на окне pygame
    """
    Класс с камерой, которая будет центрироваться на персноже
    """
    def __init__(self, target, map):
        self.target = target
        self.map = map
        self.x = target.x
        self.y = target.y

    def update(self):
        self.x = self.target.x
        self.y += self.target.y


class BaseCharacter:
    """
    Класс для основ всего 'живого'
    """
    def __init__(self, x, y, hp, name):  # x и y здесь - это на готовой карте из тайлов
        self.name = name
        self.x = x
        self.y = y
        self.hp = hp

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def is_alive(self):
        if self.hp > 0:
            return True
        return False

    def get_damage(self, hit):
        if self.is_alive():
            self.hp -= hit

    def get_coords(self):
        return self.x, self.y


class Hero(BaseCharacter):
    """
    Класс ГГ
    """
    def __init__(self, x, y, hp, name, weapon, armor, gamefield):
        super.__init__(x, y, hp, name)
        self.gamefield = gamefield
        self.weapon = weapon
        self.armor = armor
        self.inventory = [weapon, armor, []]

    def hit(self, target):
        target.get_damage(self.weapon.damage)

    def change_weapon(self, new_weapon):
        if len(self.inventory[2]) < 6: # Потом возможно поменяем вместимость
            self.inventory[2].append(self.weapon)
            self.weapon = new_weapon
            self.inventory[0] = new_weapon
        else:
            self.gamefield.search_tile(self.x, self.y).add_item(self.weapon)
            self.weapon = new_weapon
            self.inventory[0] = new_weapon

    def do_move(self, new_x, new_y):
        self.move(new_x - self.x, new_y - self.y) # Возможно потом прикрутим сюда A* для быстрых ходов


class BaseEnemy(BaseCharacter):
    """
    Здесь все враги
    """
    def __init__(self, x, y, hp, name, gamefield):
        super.__init__(x, y, hp, name)
        self.gamefield = gamefield
        if name == 'Rat':
            self.drop = None
            self.chance_of_drop = None
            self.damage = None
            pass
        elif name == "Skeleton":
            self.drop = None
            self.chance_of_drop = None
            self.damage = None

    def hit(self, target):
        target.get_damage(self.damage)

    def do_move(self, new_x, new_y):
        self.move(new_x - self.x, new_y - self.y)


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


class Text(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, text: str, font_size: int, text_color=(255, 0, 0), back_color=(255, 255, 255)):
        super().__init__()
        self.text_color, self.back_color = text_color, back_color

        font = pg.font.SysFont('Times New Roman', font_size)
        self.text = font.render(text, True, text_color)

        self.image = pg.Surface(self.text.get_size())
        self.image.fill(back_color)

        self.image.blit(self.text, ((self.image.get_width() - self.text.get_width()) // 2,
                                    (self.image.get_height() - self.text.get_height()) // 2))

        self.rect = pg.Rect(x, y, *self.image.get_size())


def set_start_win_btns(y: int, win_width: int, btn_width: int, btn_height: int, btn_count: int,
                       text_color: (int, int, int), back_color: (int, int, int)) -> pg.sprite.Group:
    """
    Генерация заданного количесва кнопок с опреденным шаблном
    """
    dist_btns = (win_width - btn_width * btn_count) // (btn_count + 1)
    btns_sprites_ = pg.sprite.Group([Button(x, x * (btn_width + dist_btns) + dist_btns, y, btn_width, btn_height,
                                            f'{x + 1} уровень', 30, text_color, back_color) for x in range(btn_count)])
    return btns_sprites_


if __name__ == '__main__':
    fps = 60

    pg.init()

    screen = pg.display.set_mode(start_win_size)
    pg.display.set_caption('Стартовое окно')

    start_btns_sprites = set_start_win_btns(300, start_win_width, start_win_btn_width, start_win_btn_height,
                                            start_win_btns_count, (0, 255, 0), (0, 0, 0))

    game_title = Text(40, 40, 'The Best Game Ever', 30, (0, 255, 0), (0, 0, 0))
    game_title.rect.x = (start_win_width - game_title.rect.width) // 2
    text_sprites = pg.sprite.Group([game_title])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in start_btns_sprites.sprites():
                        if btn.crossed(*event.pos):  # Здесь должна происходить загрузка уровня
                            print(f'Запускается {btn.index + 1} уровень')
                            break

        text_sprites.draw(screen)
        start_btns_sprites.draw(screen)

        pg.display.flip()
        screen.fill((0, 0, 0))
