import pygame

class Button:

    def __init__(self, x, y, image, scale, hoverImage = None) -> None:
        self.image_w = image.get_width()
        self.image_h = image.get_height()
        
        self.hover_w = hoverImage.get_width()
        self.hover_h = hoverImage.get_height()

        self.scale = scale

        self.image = pygame.transform.scale(image, (self.image_w * scale, self.image_h * scale))
        self.hoverImage = pygame.transform.scale(hoverImage, (self.hover_w * (scale+0.04), self.hover_h * (scale+0.04)))

        self.imageRect = self.image.get_rect()
        self.imageRect.topleft = (x,y)

        self.hoverImageRect = self.hoverImage.get_rect()
        self.hoverImageRect.topleft = (x-4*scale, y-4*scale)

    def draw(self, screen) -> int:
        """
        return 1 if pressed
        """

        pos = pygame.mouse.get_pos()

        if self.imageRect.collidepoint(pos):
            screen.blit(self.hoverImage, (self.hoverImageRect.x, self.hoverImageRect.y))
            if pygame.mouse.get_pressed()[0] == 1:
                return 1
        else:
            screen.blit(self.image, (self.imageRect.x, self.imageRect.y))