import pygame as pg
from sys import exit
import os

tile_size = (tile_width, tile_height) = (64, 64)

pg.init()
pg.mixer.music.load('data\Sounds\GAZ.mp3')  # Спасибо Тиму за музончик, мне нравится


def align(display_length: int, sprite_length: int) -> int:
    """Возвращает коррдинату для выравнивания объекта по середине"""
    return (display_length - sprite_length) // 2


def create_sprite(x: int, y: int, image: pg.Surface, step_x=0, step_y=0) -> pg.sprite.Sprite:
    sprite_ = pg.sprite.Sprite()
    sprite_.rect = pg.Rect(x * tile_width + step_x, y * tile_height + step_y, *tile_size)
    sprite_.image = image
    return sprite_


def load_image(*path) -> pg.Surface:
    fullname = os.path.join('data', *path)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):

        exit()
    image = pg.image.load(fullname)
    return image


def load_music(*path):
    fullname = os.path.join('data', *path)
    print(fullname)
    if not os.path.isfile(fullname):
        exit()
    music = pg.mixer.Sound(fullname)

    return music


def terminate() -> None:
    pg.quit()
    exit()
