from Classes.AI import *
from Classes.Camera import *
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
import random

floor_sprites = pg.sprite.Group()
wall_sprites = pg.sprite.Group()
none_sprites = pg.sprite.Group()

stone_sprites = pg.sprite.Group()
ladder_sprites = pg.sprite.Group()

enemy_sprites = pg.sprite.Group()
main_hero_sprites = pg.sprite.Group()

start_win_btn_sprites = pg.sprite.Group()
start_win_text_sprites = pg.sprite.Group()

death_win_btn_sprites = pg.sprite.Group()
death_win_text_sprites = pg.sprite.Group()

heart_sprites = pg.sprite.Group()


def clear_game_sprite_groups() -> None:
    """Очищение всех групп спрайтов"""
    floor_sprites.empty()
    wall_sprites.empty()
    none_sprites.empty()

    stone_sprites.empty()
    ladder_sprites.empty()

    enemy_sprites.empty()
    main_hero_sprites.empty()

    heart_sprites.empty()


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


def filling_sprite_groups(cell):
    """Распределение тайла в группу спрайтов"""
    if str(cell) == NONE_SIGN:  # Пустота
        none_sprites.add(cell)
    if str(cell) == FLOOR_SIGN:  # Пол
        floor_sprites.add(cell)
    if str(cell) == WALL_SIGN:  # Стена
        wall_sprites.add(cell)
    if str(cell) == STONE_SIGN:  # Камень
        floor_sprites.add(cell)
        stone_sprites.add(cell.character)
    if str(cell) == RAT_SIGN:  # Крыса
        floor_sprites.add(cell)
        enemy_sprites.add(cell.character)
    if str(cell) == HERO_SIGN:  # Главный герой
        floor_sprites.add(cell)
        main_hero_sprites.add(cell.character)
    if str(cell) == LADDER_SIGN:  # Лесница
        ladder_sprites.add(cell)
    if str(cell) == 'heart':
        heart_sprites.add(cell)


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
            Button(x_, x_ * (btn_width + dist_btns) + dist_btns, y_, btn_width, btn_height, f'Начать игру', 30,
                   text_color, back_color))
    return btns_sprites_


def set_death_win_btns(y_: int, win_width: int, btn_width: int, btn_height: int, btn_count: int,
                       text_color: (int, int, int), back_color: (int, int, int)) -> pg.sprite.Group:
    dist_btns = (win_width - btn_width * btn_count) // (btn_count + 1)
    btns_sprites_ = pg.sprite.Group()

    for x_ in range(btn_count):
        btns_sprites_.add(
            Button(x_, x_ * (btn_width + dist_btns) + dist_btns, y_, btn_width, btn_height, 'Вернуться в меню', 30,
                   text_color, back_color))
    return btns_sprites_


def make_field(lvl):
    global screen, field1, field, start_x, start_y, window, points
    clear_game_sprite_groups()
    # Изменение размера окна под игру
    screen = pg.display.set_mode(flags=pg.FULLSCREEN)
    pg.display.set_caption(f'{lvl}-й уровень')

    # Создание поля
    field1 = proc_gen(lvl)
    field = field_increase(field1.my_map)
    start_x, start_y = find_player(field, HERO_SIGN)
    set_sprites_pos(field, start_x, start_y)

    # Распределение тайлов по группам
    for y, row_ in enumerate(field):
        for x, cell in enumerate(row_):
            filling_sprite_groups(cell)

    for i in range(HERO_HP//4):
        heart_sprites.add(Heart(i, 0))

    # Изменение состояния окна
    window = 1


def heart_update(hp):
    cnt = 1
    for i in heart_sprites:
        if cnt * 4 <= hp:
            if i.state != 2:
                i.set_state(2)
        elif cnt * 4 - 2 <= hp:
            if i.state != 1:
                i.set_state(1)
        else:
            if i.state != 0:
                i.set_state(0)
        cnt += 1


if __name__ == '__main__':
    fps = 60

    pg.init()

    window = 0
    screen = pg.display.set_mode(MENU_WIN_SIZE)
    pg.display.set_caption('Стартовое окно')

    start_win_btn_sprites = set_start_win_btns(300, MENU_WIN_WIDTH, MENU_WIN_BTN_WIDTH, MENU_WIN_BTN_HEIGHT,
                                               START_WIN_BTN_COUNT, (0, 255, 0), (0, 0, 0))

    game_title = Text(40, 40, 'The Best Game Ever', 30, (0, 255, 0), (0, 0, 0))
    game_title.rect.x = align(screen.get_width(), game_title.rect.w)
    start_win_text_sprites = pg.sprite.Group([game_title])

    death_win_btn_sprites = set_death_win_btns(200, MENU_WIN_WIDTH, 400,
                                               MENU_WIN_BTN_HEIGHT,
                                               DEATH_MENU_BTN_COUNT, (0, 255, 0), (0, 0, 0))

    game_title.rect.x = align(screen.get_width(), game_title.rect.w)
    death_win_text_sprites = pg.sprite.Group(Text(200, 40, 'Вы умерли', 30, (0, 255, 0), (0, 0, 0)))
    turn = -1

    field = []
    while True:
        if window == 0:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Обработка нажаяти левой кнопки мыши
                        for btn in start_win_btn_sprites:
                            if btn.crossed(*event.pos):  # Здесь должна происходить загрузка уровня
                                lvl = 1
                                points = 0
                                make_field(lvl)
                                break

            # Отрисовка спрайтов окна меню
            start_win_text_sprites.draw(screen)
            start_win_btn_sprites.draw(screen)

        elif window == 1:
            if turn == len(field1.turns):
                turn = -1
            if not field1.hero.is_alive():  # Надо сделать переход в главное меню
                clear_game_sprite_groups()
                screen = pg.display.set_mode(MENU_WIN_SIZE)
                pg.display.set_caption('Вы умерли')

                window = 2
            if turn == -1:
                delta = ()
                action = False
                for i in pg.event.get():  # Проверяем действия игрока
                    if i.type == pg.QUIT:
                        terminate()
                    if i.type == pg.KEYDOWN:
                        if i.key == pg.K_w or i.key == pg.K_UP:
                            delta = (0, -1)
                        if i.key == pg.K_a or i.key == pg.K_LEFT:  # Дельта показывает на то, куда смещаются координаты (x, y)
                            delta = (-1, 0)
                        if i.key == pg.K_s or i.key == pg.K_DOWN:
                            delta = (0, 1)
                        if i.key == pg.K_d or i.key == pg.K_RIGHT:
                            delta = (1, 0)
                        if i.key == pg.K_e:
                            action = True  # action - если игрок взаиsмодействует с клеткой, на которой стоит
                        if i.key == pg.K_RALT:
                            field1.hero.hp = 100000
                if delta:
                    check_cell = (field1.hero.get_cell()[0] + delta[0] + 17, field1.hero.get_cell()[1] + delta[1] + 14)

                    if field1.my_map[check_cell[1]][check_cell[0]].type == 'floor':
                        if not field1.my_map[check_cell[1]][check_cell[0]].character:
                            field1.hero.move(delta[0], delta[1])  # <------ ВОТ ЗДЕСЬ КАМЕРА ДОЛЖНА ОБНОВЛЯТЬСЯ
                            for y in range(len(field)):
                                for x in range(len(field[y])):
                                    field[y][x].move(*delta)
                                    if field[y][x].character and not isinstance(field[y][x].character, MainCharacter)\
                                            or isinstance(field[y][x].character, Stone):
                                        # field[y][x].character.move(*delta)
                                        field[y][x].character.move_tile(*delta)

                            field1.my_map[field1.hero.get_cell()[1] + 14 - delta[1]][
                                field1.hero.get_cell()[0] + 17 - delta[0]].add_character(None)
                            field1.my_map[check_cell[1]][check_cell[0]].add_character(
                                field1.hero)  # Если на полу ничего нет, то он идёт
                            WALK_SND.play()
                        elif isinstance(field1.my_map[check_cell[1]][check_cell[0]].character, Stone):
                            stone_sprites.remove(field1.my_map[check_cell[1]][check_cell[0]].character)
                            field1.my_map[check_cell[1]][check_cell[0]].add_character(
                                None)  # Если там камень, то он ломает его
                            field1.hero.hp += random.randint(0, 1)
                            if not random.randint(0, 5):
                                points += 1
                            BREAK_STONE_SND.play()
                        elif isinstance(field1.my_map[check_cell[1]][check_cell[0]].character, BaseEnemy):
                            field1.hero.hit(field[check_cell[1]][check_cell[0]].character)  # Если враг, то бьёт его
                            if not field[check_cell[1]][check_cell[0]].character.is_alive():
                                field[check_cell[1]][check_cell[0]].character.death_snd.play()
                                points += field[check_cell[1]][check_cell[0]].character.points
                                enemy_sprites.remove(field[check_cell[1]][check_cell[0]].character)
                                field1.turns.remove(field[check_cell[1]][check_cell[0]].character)
                                field1.my_map[check_cell[1]][check_cell[0]].add_character(None)
                                field1.hero.hp += random.randint(1, 4)
                            else:
                                HIT_SND.play()
                    elif field1.my_map[check_cell[1]][check_cell[0]].type == 'ladder':
                        if isinstance(field1.my_map[check_cell[1]][check_cell[0]].character, BaseEnemy):
                            field1.hero.hit(field[check_cell[1]][check_cell[0]].character)  # Если враг, то бьёт его

                            if not field[check_cell[1]][check_cell[0]].character.is_alive():
                                field[check_cell[1]][check_cell[0]].character.death_snd.play()
                                enemy_sprites.remove(field[check_cell[1]][check_cell[0]].character)
                                field1.turns.remove(field[check_cell[1]][check_cell[0]].character)
                                field1.my_map[check_cell[1]][check_cell[0]].add_character(None)
                            else:
                                HIT_SND.play()
                        else:
                            points += lvl * 10
                            lvl += 1
                            make_field(lvl)  # Если лестница, то идёт на следующий уровень
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

                delta = calculate_turn(enemy, field1)
                if delta == 'upd':
                    heart_update(field1.hero.hp)
                elif delta:

                    check_cell = (enemy.get_cell()[0] + delta[0] + 17, enemy.get_cell()[1] + delta[1] + 14)
                    if field1.my_map[check_cell[1]][check_cell[0]].type in ('floor', 'ladder'):
                        if not field1.my_map[check_cell[1]][check_cell[0]].character:

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

            heart_sprites.draw(screen)

        if window == 2:
            f = open('record.txt')
            try:
                record = int(f.read())
            except:
                record = -1
            f.close()
            if record < points:
                WIN_SND.play()
                f = open('record.txt', 'w')
                f.write(str(points))
                f.close()
                record = points
            death_win_text_sprites.add(Text(40, 130, f'Ваш счёт: {points}, рекорд: {record}', 30, (0, 255, 0), (0, 0, 0)))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for btn in death_win_btn_sprites:
                            if btn.crossed(*event.pos):
                                death_win_text_sprites = pg.sprite.Group(
                                    Text(200, 40, 'Вы умерли', 30, (0, 255, 0), (0, 0, 0)))
                                pg.display.set_caption('Стартовое окно')
                                window = 0

            death_win_text_sprites.draw(screen)
            death_win_btn_sprites.draw(screen)

        pg.display.flip()
        screen.fill((0, 0, 0))
