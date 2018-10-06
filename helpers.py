import pygame


class CustomSprite(pygame.sprite.Sprite):
    """pygame.Sprite with pixel bitmask collision detection"""
    def __init__(self):
        super().__init__()

    """ get bit mask from image """
    def get_bitmask(self):
        mask = []
        for x in range(self.image.get_width()):
            mask.append([])
            for y in range(self.image.get_height()):
                mask[x].append(bool(self.image.get_at((x, y))[3]))
        return mask

    """ check for collision with other based on  bitmask"""
    def pixel_collide(self, other):
        # rectangle cross section of this sprite with other
        rect = self.rect.clip(other.rect)
        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - self.rect.x, rect.y - self.rect.y
        x2, y2 = rect.x - other.rect.x, rect.y - other.rect.y

        # check every pixel in the cross section for collision
        # i.e both bit are True
        bitmask1 = self.get_bitmask()
        bitmask2 = other.get_bitmask()
        for x in range(rect.width):
            for y in range(rect.height):
                if bitmask1[x1 + x][y1 + y] and bitmask2[x2 + x][y2 + y]:
                    return True
        return False
