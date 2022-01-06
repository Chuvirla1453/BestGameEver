import pygame as pg
import os


def load_image(name: str):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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
        super(Tile, self).__init__()

        self.image = load_image(image)
        self.rect = pg.Rect(x * self.image.get_width(), y * self.image.get_height(), *self.image.get_size())
