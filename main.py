from classes.AI import *
from classes.Cells import *
from classes.Characters import *
from classes.Errors import *
from classes.Consts import *
from classes.Menu_elements import *
from classes.Proc_gen import proc_gen
from classes.Secondary_functions import *

import pygame as pg
from math import ceil

floor_sprites = pg.sprite.Group()
wall_sprites = pg.sprite.Group()
none_sprites = pg.sprite.Group()

stone_sprites = pg.sprite.Group()
ladder_sprites = pg.sprite.Group()

enemy_sprites = pg.sprite.Group()
main_hero_sprites = pg.sprite.Group()

sprite_groups = floor_sprites, wall_sprites, none_sprites, stone_sprites, ladder_sprites, enemy_sprites


def set_start_win_btns(y: int, win_width: int, btn_width: int, btn_height: int, btn_count: int,
                       text_color: (int, int, int), back_color: (int, int, int)) -> pg.sprite.Group:
    """
    Генерация заданного количесва кнопок с опреденным шаблном
    """
    dist_btns = (win_width - btn_width * btn_count) // (btn_count + 1)
    btns_sprites_ = pg.sprite.Group([Button(x, x * (btn_width + dist_btns) + dist_btns, y, btn_width, btn_height,
                                            f'{x + 1} уровень', 30, text_color, back_color) for x in range(btn_count)])
    return btns_sprites_


def clear_all_sprite_groups() -> None:
    """Очищение всех групп спрайтов"""
    floor_sprites.empty()
    wall_sprites.empty()
    none_sprites.empty()

    stone_sprites.empty()
    ladder_sprites.empty()

    enemy_sprites.empty()
    main_hero_sprites.empty()


def field_increase(field):
    """
    Увеличение игрового поля спрайтами пустоты, чтобы не было пустых зон
    """
    for i_ in range(len(field)):
        if field[i_]:
            field[i_] = ['.'] * 17 + field[i_] + ['.'] * 17
        else:
            field[i_] = ['.'] * len(field[i_ - 1])

    return list(map(lambda x: ['.'] * len(field[0]), range(14))) + field + list(
        map(lambda x: ['.'] * len(field[0]), range(14)))


def find_player(field: list, player_sign: str) -> (int, int):
    """
    Функция игрока на поле и возвращает координату клетки
    """
    player = None
    for y_, row_ in enumerate(field):
        if player_sign in row_:
            if player is None:
                player = (row_.index(player_sign), y_)
            else:
                raise MultiplicityPlayersError('Несколько игроков на поле')

    if player is None:
        raise PlayerNotFoundError('Игрок не обнаружен на поле')
    return player


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

    sprite_field = []
    str_field = []

    while True:
        if window == 0:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1: # Обработка нажаяти левой кнопки мыши
                        for btn in start_btns_sprites:
                            if btn.crossed(*event.pos):  # Здесь должна происходить загрузка уровня
                                # Изменение размера окна под игру
                                screen = pg.display.set_mode(flags=pg.FULLSCREEN)
                                pg.display.set_caption(f'{btn.index + 1}-й уровень')

                                # Создание поля
                                str_field = field_increase(
                                    list(map(lambda i: list(map(lambda j: str(j), i)), proc_gen(btn.index + 1).my_map)))
                                for i in str_field:
                                    print(*i)
                                start_x, start_y = find_player(str_field, 'C')

                                clear_all_sprite_groups()

                                # Создание спрайтов тайлов
                                for y, row in enumerate(str_field):
                                    y = y - start_y + ceil(screen.get_width() / tile_width / 3)
                                    for x, cell in enumerate(row):
                                        x = x - start_x + ceil(screen.get_height() / tile_height / 2)

                                        if cell == NONE_SIGN:
                                            none_sprites.add(Tile(x, y, 'none'))
                                        if cell == FLOOR_SIGN:
                                            floor_sprites.add(Tile(x, y, 'floor'))
                                        if cell == WALL_SIGN:
                                            wall_sprites.add(Tile(x, y, 'wall'))
                                        if cell == STONE_SIGN:
                                            floor_sprites.add(Tile(x, y, 'floor'))
                                            stone_sprites.add(Tile(x, y, 'stone'))
                                        if cell == RAT_SIGN:
                                            some_tile = Tile(x, y, 'floor')
                                            some_tile.character = BaseEnemy(x, y, RAT_SPRITE, RAT_HP,
                                                                            RAT_DAMAGE, RAT_ARMOR, 'Крыса', -1)
                                            floor_sprites.add(some_tile)
                                            enemy_sprites.add(some_tile.character)
                                        if cell == HERO_SIGN:
                                            some_tile = Tile(x, y, 'floor')
                                            some_tile.character = MainCharacter(x, y, HERO_HP, 'GG', -1, -1, -1)

                                            floor_sprites.add(some_tile)
                                            main_hero_sprites.add(some_tile.character)
                                        if cell == LADDER_SIGN:
                                            some_tile = Tile(x, y, 'floor')
                                            some_tile.character = Tile(x, y, 'ladder')

                                            floor_sprites.add(some_tile)
                                            ladder_sprites.add(some_tile.character)

                                # Изменение состояния окна
                                window = 1
                                break

            # Отрисовка спрайтов окна
            text_sprites.draw(screen)
            start_btns_sprites.draw(screen)

        elif window == 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()

            # Отрисовка спрайтов игровго окна
            floor_sprites.draw(screen)
            wall_sprites.draw(screen)
            none_sprites.draw(screen)

            stone_sprites.draw(screen)
            ladder_sprites.draw(screen)

            enemy_sprites.draw(screen)
            main_hero_sprites.draw(screen)

        pg.display.flip()
        screen.fill((0, 0, 0))
