import pygame


class Pipe():
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += -4
