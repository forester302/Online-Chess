import pygame

from Components.Screen.ScreenObjects.ScreenObject import ScreenObject

pygame.font.init()


class Text(ScreenObject):
    def __init__(self, font, size, text, pos: tuple[int, int] = (0, 0), colour: tuple[int, int, int] = (0, 0, 0)):
        # Initialize the text object's font, size, text, position, and color
        self.size = size
        self.pos = pos
        self.text = text
        self.font = font
        self.font = pygame.font.SysFont(self.font, self.size)
        self.textcolour = colour
        self.render = []
        self.position = 'Center'
        super().__init__(0, 0, 0, 0)

    def make_rect(self, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)):
        # Create the text surface and align it to the rect
        self._rendertext()
        self._align(rect)

    def _rendertext(self):
        # Create the text surface
        temptext = self.text.split("\n")
        self.render = []
        for text in temptext:
            self.render.append(self.font.render(text, False, self.textcolour))

    def _align(self, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)):
        # Align the text according to the position variable
        sizex, sizey = rect.size
        if self.position == 'Left':
            self.position_left((rect.x + sizex / 6, rect.y + (sizey / 2)))
        elif self.position == 'Center':
            self.position_center((rect.x + (sizex / 2), rect.y + (sizey / 2)))
        elif self.position == 'Right':
            self.position_right((rect.x + sizex - (sizex / 6), rect.y + (sizey / 2)))

    def position_left(self, pos):
        # Position the text to the left of the given position
        self.position = 'Left'
        length = len(self.render)
        mid = length / 2
        mid = round(mid)
        rect = self.render[mid].get_rect()
        rect.midleft = pos
        self.pos = rect.topleft

    def position_right(self, pos):
        # Position the text to the right of the given position
        self.position = 'Right'
        length = len(self.render)
        mid = length / 2
        mid = round(mid)
        rect = self.render[mid].get_rect()
        rect.midright = pos
        self.pos = rect.topleft

    def position_center(self, pos):
        # Position the text in the center of the given position
        self.position = 'Center'
        length = len(self.render)
        mid = length / 2
        mid = round(mid)
        rect = self.render[mid].get_rect()
        rect.center = pos
        self.pos = rect.topleft

    def draw(self, screen):
        # Draw the text surface to the screen
        for i in range(0, len(self.render)):
            screen.blit(self.render[i], (self.pos[0], self.pos[1] + (self.size * i)))
