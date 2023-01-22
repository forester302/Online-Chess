import pygame

from Components.Screen.ScreenObjects.ScreenObject import ScreenObject


class Hover(ScreenObject):
    def __init__(self, x, y, sizex, sizey, colour: tuple[int, int, int] = (0, 0, 0),
                 hovercolour: tuple[int, int, int] = (0, 0, 0)):
        # Initialize the object's x and y position, size, color, and hover color
        super().__init__(x, y, sizex, sizey, colour)
        self.hovercolour = hovercolour
        self.maincolour = colour

    def check_mouse(self, pos: tuple[int, int]):
        # Check if the mouse is over the object, and change the color if it is
        if super().check_mouse(pos):
            self.colour = self.hovercolour
            return True
        else:
            self.colour = self.maincolour
            return False

class Button(Hover):
    def __init__(self, x, y, sizex, sizey, script, scriptparam=None, colour: tuple = (0, 0, 0),
                 hovercolour: tuple = (0, 0, 0)):
        # Initialize the button's x and y position, size, color, hover color, script and script parameter
        super().__init__(x, y, sizex, sizey, colour, hovercolour)
        self.script = script
        self.scriptparam = scriptparam

    def click(self):
        # Handle a click event on the button, and call the script with script parameter
        for obj in self._objects.values():
            obj.click()
        if not self.check_mouse(pygame.mouse.get_pos()):
            return
        if self.scriptparam is not None:
            self.script(self.scriptparam)
            return
        self.script()
