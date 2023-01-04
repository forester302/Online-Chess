import pygame
from Components.Screen.ScreenObjects.ScreenObject import ScreenObject


class Screen:
    _objects: dict[str, ScreenObject] = {}
    screen = None

    def __init__(self, size, framerate: int = 60, bgcolour: tuple = (0, 0, 0)):
        self.size = size
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.bgcolour = bgcolour

    def make_screen(self):
        self.screen = pygame.display.set_mode(self.size)
        self.draw()

    def tick(self):
        self.clock.tick(self.framerate)

    def add_object(self, name: str, object: ScreenObject):
        self._objects[name] = object

    def del_object(self, name: str):
        self._objects.pop(name)

    def get_object(self, name: str):
        return self._objects[name]

    def check_open(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self._objects.values():
                    obj.click()
            if event.type == pygame.KEYDOWN:
                for obj in self._objects.values():
                    obj.key_down(event)
            for obj in self._objects.values():
                obj.check_mouse(pygame.mouse.get_pos())
        return True

    def draw(self):
        self.screen.fill(self.bgcolour)
        for obj in self._objects.values():
            obj.draw(self.screen)
        pygame.display.flip()