import pygame

from Components.Screen.ScreenObjects.ScreenObject import ScreenObject
from Components.Screen.ScreenObjects.Text import Text


class TextBox(ScreenObject):
    def __init__(self, x, y, sizex, sizey, *, colour: tuple = (0, 0, 0), textcolour: tuple = (0, 0, 0),
                 font: str = 'Century', textsize: int = 30, characterlimit: int = 2048, newline: bool = True):
        # Initialize the base class and set the color of the textbox
        super().__init__(x, y, sizex, sizey, colour)

        # Initialize the text object and position it inside the textbox
        self.text = Text(font, textsize, "", (x + 10, y + 10), textcolour)
        self._objects["text"] = self.text
        self.text.position_left((0, 0))

        # Set the character limit and whether newlines are allowed
        self.characterlimit = characterlimit
        self.newline = newline
        self.selected = False

    def key_down(self, event):
        # Check if the textbox is selected and handle the key press
        if self.selected:
            if event.key == pygame.K_BACKSPACE:
                self.text.text = self.text.text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.newline:
                    self.text.text += "\n"
            elif event.key == pygame.K_v:
                if not pygame.scrap.get_init():
                    pygame.scrap.init()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL]:
                    text = str(pygame.scrap.get(pygame.SCRAP_TEXT))
                    text = text[:-5]
                    text = text[2:]
                    self.text.text += str(text)
                else:
                    if len(self.text.text) < self.characterlimit:
                        self.text.text += event.unicode
            else:
                if len(self.text.text) < self.characterlimit:
                    self.text.text += event.unicode
            self.text.make_rect(self.rect)

    def click(self):
        # Handle clicking on the textbox
        pos = pygame.mouse.get_pos()
        if super().check_mouse(pos):
            self.selected = True
        else:
            self.selected = False