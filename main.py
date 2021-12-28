import pygame as pg
from sys import exit


start_win_size = (start_win_width, start_win_height) = (600, 400)

start_win_btn_size = (start_win_btn_width, start_win_btn_height) = (140, 70)
start_win_btns_count = 3


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
