import pygame as pg


class Button(pg.sprite.Sprite):
    """Класс кнопки, для удобной работы в меню"""

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
        """Отрисовка текста и узора кнопки"""
        self.image.fill(self.back_color)
        self.image.blit(self.text, (self.rect.width // 2 - self.text.get_width() // 2,
                                    self.rect.height // 2 - self.text.get_height() // 2))

        for i in range(len(self.extreme_points)):
            pg.draw.line(self.image, self.text_color, self.extreme_points[i],
                         self.extreme_points[(i + 1) % len(self.extreme_points)], width=5)

    def crossed(self, x: int, y: int) -> bool:
        """Проверка, назодится ди координата в диапозоне координат кнопки"""
        return self.rect.collidepoint(x, y)


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
