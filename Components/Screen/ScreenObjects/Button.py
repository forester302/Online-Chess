import pygame

from Components.Screen.ScreenObjects.ScreenObject import ScreenObject


class Hover(ScreenObject):
    def __init__(self, x, y, sizex, sizey, colour: tuple[int, int, int] = (0, 0, 0),
                 hovercolour: tuple[int, int, int] = (0, 0, 0)):
        super().__init__(x, y, sizex, sizey, colour)
        self.hovercolour = hovercolour
        self.maincolour = colour

    def check_mouse(self, pos: tuple[int, int]):
        if super().check_mouse(pos):
            self.colour = self.hovercolour
            return True
        else:
            self.colour = self.maincolour
            return False


class Button(Hover):
    def __init__(self, x, y, sizex, sizey, script, scriptparam=None, colour: tuple = (0, 0, 0),
                 hovercolour: tuple = (0, 0, 0)):
        super().__init__(x, y, sizex, sizey, colour, hovercolour)
        self.script = script
        self.scriptparam = scriptparam

    def click(self):
        for obj in self._objects.values():
            obj.click()
        if not self.check_mouse(pygame.mouse.get_pos()):
            return
        if self.scriptparam is not None:
            self.script(self.scriptparam)
            return
        self.script()
