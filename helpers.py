import pygame


class SpriteWithHitmask(pygame.sprite.Sprite):
    """pygame.Sprite with pixel bitmask collision detection"""
    def __init__(self):
        super().__init__()

    """ get bit mask from image """
    def get_hitmask(self, img):
        mask = []
        for x in range(img.get_width()):
            mask.append([])
            for y in range(img.get_height()):
                mask[x].append(bool(img.get_at((x, y))[3]))
        return mask

    """ check for collision with other based on  bitmask"""
    def pixel_collide(self, other):
        # Rectangle cross section of this sprite with other
        rect = self.rect.clip(other.rect)
        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - self.rect.x, rect.y - self.rect.y
        x2, y2 = rect.x - other.rect.x, rect.y - other.rect.y

        # Check every pixel in the cross section for collision
        # i.e both bit are True
        for x in range(rect.width):
            for y in range(rect.height):
                if self.hitmask[x1 + x][y1 + y] and other.hitmask[x2 + x][y2 + y]:
                    return True
        return False
