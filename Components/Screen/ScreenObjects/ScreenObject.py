import pygame


class ScreenObject:
    def __init__(self, x: int, y: int, sizex: int, sizey: int, colour: tuple[int, int, int] = (0, 0, 0)):
        # Initialize the object's x and y position, size, and color
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.rect = None
        self._objects: dict[str: ScreenObject] = {}
        self.make_rect()
        self.colour = colour

    def make_rect(self, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)):
        # Create the object's rectangle, and update the rectangles of any child objects
        topleft = rect.topleft
        self.rect = pygame.Rect(self.x + topleft[0], self.y + topleft[1], self.sizex, self.sizey)
        for obj in self._objects.values():
            obj.make_rect(self.rect)

    def draw(self, screen):
        # Draw the object's rectangle, and any child objects
        pygame.draw.rect(screen, self.colour, self.rect)
        for obj in self._objects.values():
            obj.draw(screen)

    def check_mouse(self, pos: tuple[int, int]):
        # Check if the mouse is over the object, and check any child objects
        for obj in self._objects.values():
            obj.check_mouse(pos)
        if self.rect is not None and self.rect.collidepoint(pos[0], pos[1]):
            return True
        return False

    def click(self):
        # Handle a click event on the object and any child objects
        for obj in self._objects.values():
            obj.click()

    def add_child(self, name: str, obj):
        # Add a child object to the object
        self._objects[name] = obj
        obj.make_rect(self.rect.topleft)

    def add_text(self, name: str, font: str, size: int, text: str, colour: tuple[int, int, int] = (0, 0, 0),
                 centre: bool = False, left: bool = False, right: bool = False):
        # Add text to the object
        textobj = Text(font=font, size=size, text=text, colour=colour)
        if left:
            textobj.position_left((self.rect.x + size / 6, self.rect.y + (self.sizey / 2)))
        elif right:
            textobj.position_right((self.rect.x + self.sizex - (size / 6), self.rect.y + (self.sizey / 2)))
        elif centre or True:
            textobj.position_center((self.rect.x + (self.sizex / 2), self.rect.y + (self.sizey / 2)))
        self._objects[name] = textobj

    def key_down(self, event):
        pass


from Components.Screen.ScreenObjects.Text import Text
