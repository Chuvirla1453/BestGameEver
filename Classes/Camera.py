from pygame.sprite import Sprite


class Camera:
    """Класс для сдвига объектов по координатам"""
    def __init__(self, x_step: int, y_step: int):
        self.step_x, self.step_y = x_step, y_step

    def apply(self, obj, x_fac: int, y_fac: int):
        """Функция сдвигает объектов по координатам."""

        if not (issubclass(type(obj), Sprite) or isinstance(obj, Sprite)):
            raise TypeError('Объект должен быть унаследован от pygame.sprite.Sprite или являться им.')
        obj.rect.x += x_fac * self.step_x
        obj.rect.y += y_fac * self.step_y
