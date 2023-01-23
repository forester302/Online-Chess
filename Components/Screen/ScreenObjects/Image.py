import pygame

from Components.Screen.ScreenObjects.ScreenObject import ScreenObject


class Image(ScreenObject):
    def __init__(self, x: int, y: int, sizex: int, sizey: int, image_path: str):
        super().__init__(x, y, sizex, sizey)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (sizex, sizey))

    def draw(self, screen: pygame.Surface):
        # Draw the image on the screen surface at the rectangle position.
        screen.blit(self.image, self.rect)
