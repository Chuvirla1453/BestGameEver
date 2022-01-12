from Classes.AI import *
# from classes.Cells import *
# from classes.Characters import *
from Classes.Errors import *
from Classes.Game_cycle import *
from Classes.Consts import *
from Classes.Menu_elements import *
from Classes.Proc_gen import proc_gen
from Classes.Secondary_functions import *

import pygame as pg
from math import ceil

floor_sprites = pg.sprite.Group()
wall_sprites = pg.sprite.Group()
none_sprites = pg.sprite.Group()

stone_sprites = pg.sprite.Group()
ladder_sprites = pg.sprite.Group()

enemy_sprites = pg.sprite.Group()
main_hero_sprites = pg.sprite.Group()

sprite_groups = (floor_sprites, wall_sprites, none_sprites, stone_sprites, ladder_sprites, enemy_sprites)


def clear_all_sprite_groups() -> None:
    """Очищение всех групп спрайтов"""
    floor_sprites.empty()
    wall_sprites.empty()
    none_sprites.empty()

    stone_sprites.empty()
    ladder_sprites.empty()

    enemy_sprites.empty()
    main_hero_sprites.empty()


def field_increase(field_: list):
    """
    Увеличение игрового поля спрайтами пустоты, чтобы не было пустых зон
    """
    for i_ in range(len(field_)):  # Добавление ктолок по бокам
        if field_[i_]:
            for j in range(17):
                field_[i_].insert(0, Tile(-1, -1, 'none'))
                field_[i_].append(Tile(-1, -1, 'none'))
        else:
            field_[i_] = [Tile(-1, -1, 'none') for i in range(len(field_[0]))]

    for i_ in range(14):  # Добавление клеток сверху и снизу
        field_.insert(0, list(map(lambda x: Tile(-1, -1, 'none'), range(len(field_[1])))))
        field_.insert(len(field_), list(map(lambda x: Tile(-1, -1, 'none'), range(len(field_[1])))))

    return field_


def filling_sprite_groups(cell_):
    """Распределение тайла в группу спрайтов"""
    if str(cell_) == NONE_SIGN:  # Пустота
        none_sprites.add(cell)
    if str(cell_) == FLOOR_SIGN:  # Пол
        floor_sprites.add(cell)
    if str(cell_) == WALL_SIGN:  # Стена
        wall_sprites.add(cell)
    if str(cell_) == STONE_SIGN:  # Камень
        floor_sprites.add(cell)
        stone_sprites.add(cell.character)
    if str(cell_) == RAT_SIGN:  # Крыса
        floor_sprites.add(cell)
        enemy_sprites.add(cell.character)
    if str(cell_) == HERO_SIGN:  # Главный герой
        floor_sprites.add(cell)
        main_hero_sprites.add(cell.character)
    if str(cell_) == LADDER_SIGN:  # Лесница
        ladder_sprites.add(cell)


def find_player(field_: list, player_sign_: str) -> (int, int):
    """
    Функция поиска игрока на поле и возвращает координату клетки
    """
    player = None
    for y_, row_ in enumerate(field_):
        for x_, cell_ in enumerate(row_):
            if str(cell_) == player_sign_:
                if player is None:
                    player = (x_, y_)
                else:
                    raise MultiplicityPlayersError('Несколько игроков на поле')

    if player is None:
        raise PlayerNotFoundError('Игрок не обнаружен на поле')
    return player


def set_sprites_pos(field_: list, s_x: int, s_y: int):
    """Установка координат тайлов по отношению к позтции ГГ"""
    for y_, row_ in enumerate(field_):
        y_ = y_ - s_y + ceil(screen.get_width() // tile_width // 4)

        for x_, cell_ in enumerate(row_):
            x_ = x_ - s_x + ceil(screen.get_height() // TILE_HEIGHT)

            cell_.set_pos(x_, y_)
            if cell_.character is not None:
                cell_.character.set_pos(x_, y_)


def set_start_win_btns(y_: int, win_width: int, btn_width: int, btn_height: int, btn_count: int,
                       text_color: (int, int, int), back_color: (int, int, int)) -> pg.sprite.Group:
    """
    Генерация заданного количесва кнопок с опреденным шаблном
    """
    dist_btns = (win_width - btn_width * btn_count) // (btn_count + 1)
    btns_sprites_ = pg.sprite.Group()

    for x_ in range(btn_count):
        btns_sprites_.add(
            Button(x_, x_ * (btn_width + dist_btns) + dist_btns, y_, btn_width, btn_height, f'{x_ + 1} уровень', 30,
                   text_color, back_color))
    return btns_sprites_


if __name__ == '__main__':
    fps = 60

    pg.init()

    window = 0
    screen = pg.display.set_mode(START_WIN_SIZE)
    pg.display.set_caption('Стартовое окно')

    start_btns_sprites = set_start_win_btns(300, start_win_width, start_win_btn_width, start_win_btn_height,
                                            START_WIN_SIZE_COUNT, (0, 255, 0), (0, 0, 0))

    game_title = Text(40, 40, 'The Best Game Ever', 30, (0, 255, 0), (0, 0, 0))
    game_title.rect.x = align(screen.get_width(), game_title.rect.w)
    text_sprites = pg.sprite.Group([game_title])
    turn = -1

    field = []

    while True:
        if window == 0:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Обработка нажаяти левой кнопки мыши
                        for btn in start_btns_sprites:
                            if btn.crossed(*event.pos):  # Здесь должна происходить загрузка уровня
                                clear_all_sprite_groups()
                                # Изменение размера окна под игру
                                screen = pg.display.set_mode(flags=pg.FULLSCREEN)
                                pg.display.set_caption(f'{btn.index + 1}-й уровень')

                                # Создание поля
                                field1 = proc_gen(btn.index + 1)
                                field = field_increase(field1.my_map)
                                start_x, start_y = find_player(field, HERO_SIGN)
                                set_sprites_pos(field, start_x, start_y)

                                # Распределение тайлов по группам
                                for y, row_ in enumerate(field):
                                    for x, cell in enumerate(row_):
                                        filling_sprite_groups(cell)

                                # Изменение состояния окна
                                window = 1
                                break

            # Отрисовка спрайтов окна меню
            text_sprites.draw(screen)
            start_btns_sprites.draw(screen)

        elif window == 1:
            if turn == len(field1.turns):
                turn = -1
            if not field1.hero.is_alive():
                terminate()
            if turn == -1:
                delta = ()
                action = False
                for i in pg.event.get():  # Проверяем действия игрока
                    if i.type == pg.QUIT:
                        terminate()
                    if i.type == pg.KEYDOWN:
                        if i.key == pg.K_w or i.type == pg.K_UP:
                            delta = (0, -1)
                        if i.key == pg.K_a or i.type == pg.K_LEFT:  # Дельта показывает на то, куда смещаются координаты (x, y)
                            delta = (-1, 0)
                        if i.key == pg.K_s or i.type == pg.K_DOWN:
                            delta = (0, 1)
                        if i.key == pg.K_d or i.type == pg.K_RIGHT:
                            delta = (1, 0)
                        if i.key == pg.K_e:
                            action = True  # action - если игрок взаиsмодействует с клеткой, на которой стоит
                if delta:
                    check_cell = (field1.hero.get_cell()[0] + delta[0] + 17, field1.hero.get_cell()[1] + delta[1] + 14)

                    if field1.my_map[check_cell[1]][check_cell[0]].type == 'floor':
                        if not field1.my_map[check_cell[1]][check_cell[0]].character:
                            field1.hero.move(delta[0], delta[1])  #<------ ВОТ ЗДЕСЬ КАМЕРА ДОЛЖНА ОБНОВЛЯТЬСЯ
                            field1.my_map[field1.hero.get_cell()[1] + 14 - delta[1]][field1.hero.get_cell()[0] + 17 - delta[0]].add_character(None)
                            field1.my_map[check_cell[1]][check_cell[0]].add_character(
                                field1.hero)  # Если на полу ничего нет, то он идёт
                            WALK_SND.play()
                            print(f"HERO {(field1.hero.get_cell()[0] + 17, field1.hero.get_cell()[1] + 14)}")
                        elif isinstance(field1.my_map[check_cell[1]][check_cell[0]].character, Stone):
                            stone_sprites.remove(field1.my_map[check_cell[1]][check_cell[0]].character)
                            field1.my_map[check_cell[1]][check_cell[0]].add_character(None)  # Если там камень, то он ломает его
                            BREAK_STONE_SND.play()
                        elif isinstance(field1.my_map[check_cell[1]][check_cell[0]].character, BaseEnemy):
                            field1.hero.hit(field[check_cell[1]][check_cell[0]].character)  # Если враг, то бьёт его
                            print(f"HP {field[check_cell[1]][check_cell[0]].character.hp}, {field[check_cell[1]][check_cell[0]].character.is_alive()}")
                            if not field[check_cell[1]][check_cell[0]].character.is_alive():
                                field[check_cell[1]][check_cell[0]].character.death_snd.play()
                                enemy_sprites.remove(field[check_cell[1]][check_cell[0]].character)
                                field1.turns.remove(field[check_cell[1]][check_cell[0]].character)
                                field1.my_map[check_cell[1]][check_cell[0]].add_character(None)
                            else:
                                HIT_SND.play()
                    elif field1.my_map[check_cell[1]][check_cell[0]].type == 'ladder':
                        new_level()  # Если лестница, то идёт на следующий уровень
                        LADDER_SND.play()
                    else:
                        WALK_IN_WALL_SND.play()  # Если стена, то пропускает свой ход, с помощью этого тупого действия
                    turn += 1
                elif action:
                    check_cell = field1.hero.get_cell()
                    if not field1.my_map[check_cell[1]][
                        check_cell[0]].has_item():  # Если ничего на полу нет, то тоже пропускает ход
                        WALK_IN_WALL_SND.play()
                    else:
                        PICK_SND.play()  # Если что-то есть, то распределяется в инвентарь
                        if isinstance(field1.my_map[check_cell[1]][check_cell[0]].inventory[-1], Weapon):
                            field1.hero.change_weapon(field1[check_cell[1]][check_cell[0]].inventory[-1])
                        elif isinstance(field1.my_map[check_cell[1]][check_cell[0]].inventory[-1], Armor):
                            field1.hero.change_armor(field1[check_cell[1]][check_cell[0]].inventory[-1])
                    turn += 1
            else:
                enemy = field1.turns[turn]
                print("Enemy", enemy.get_cell()[0] + 17, enemy.get_cell()[1] + 14)
                delta = calculate_turn(enemy, field1)
                if delta:
                    print("DELTA", delta)
                    check_cell = (enemy.get_cell()[0] + delta[0] + 17, enemy.get_cell()[1] + delta[1] + 14)
                    if field1.my_map[check_cell[1]][check_cell[0]].type in ('floor', 'ladder'):
                        if not field1.my_map[check_cell[1]][check_cell[0]].character:
                            print('ok')
                            enemy.move(delta[0], delta[1])
                            field1.my_map[enemy.get_cell()[1] + 14 - delta[1]][
                                enemy.get_cell()[0] + 17 - delta[0]].add_character(None)
                            field1.my_map[check_cell[1]][check_cell[0]].add_character(
                                enemy)  # Если на полу ничего нет, то он идёт
                            enemy.walk_snd.play()
                        elif isinstance(field1.my_map[check_cell[1]][check_cell[0]].character, Stone):
                            stone_sprites.remove(field1.my_map[check_cell[1]][check_cell[0]].character)
                            field1.my_map[check_cell[1]][check_cell[0]].add_character(
                                None)  # Если там камень, то он ломает его
                            BREAK_STONE_SND.play()
                        elif isinstance(field1.my_map[check_cell[1]][check_cell[0]].character, BaseEnemy):
                            pass
                    else:
                        pass
                turn += 1

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
