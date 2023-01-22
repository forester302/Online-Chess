import pygame
from Components.Screen.ScreenObjects.ScreenObject import ScreenObject


class Screen:
    def __init__(self, size, framerate: int = 60, bgcolour: tuple = (0, 0, 0)):
        # Initialize screen size, clock, framerate, background color, and object dictionary
        self.size = size
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.bgcolour = bgcolour
        self._objects: dict[str, ScreenObject] = {}
        self.screen = None
        self.enabled = False

    def make_screen(self):
        # Enable the screen and create it using the pygame display module
        self.enabled = True
        self.screen = pygame.display.set_mode(self.size)
        self.draw()

    def hide_screen(self):
        self.enabled = False

    def tick(self):
        self.clock.tick(self.framerate)

    def add_object(self, name: str, object: ScreenObject):
        # Add an object to the object dictionary
        self._objects[name] = object

    def del_object(self, name: str):
        # Remove an object from the object dictionary
        self._objects.pop(name)

    def get_object(self, name: str):
        return self._objects[name]

    def check_open(self):
        # Check if the screen is open, and handle events such as clicks and key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in self._objects.values():
                    obj.click()
                    if not self.enabled: break
            if event.type == pygame.KEYDOWN:
                for obj in self._objects.values():
                    obj.key_down(event)
                    if not self.enabled: break
            for obj in self._objects.values():
                obj.check_mouse(pygame.mouse.get_pos())
                if not self.enabled: break

        return True

    def draw(self):
        # Draw the background color and all objects in the object dictionary
        self.screen.fill(self.bgcolour)
        for obj in self._objects.values():
            obj.draw(self.screen)
        pygame.display.flip()