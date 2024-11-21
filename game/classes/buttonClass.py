import pygame

class Button:

    def __init__(self, x, y, image, scale, hoverImage = None, hoverType = 0) -> None:
        self.image_w = image.get_width()
        self.image_h = image.get_height()
        
        self.scale = scale

        if hoverImage != None:
            self.hover_w = hoverImage.get_width()
            self.hover_h = hoverImage.get_height()

            if hoverType == 1:
                self.hoverImage = pygame.transform.scale(hoverImage, (self.hover_w * (scale+0.04), self.hover_h * (scale+0.04)))
                self.hoverImageRect = self.hoverImage.get_rect()
                self.hoverImageRect.topleft = (x-4*scale, y-4*scale)
            
            else:
                self.hoverImage = pygame.transform.scale(hoverImage, (self.hover_w * (scale), self.hover_h * (scale)))
                self.hoverImageRect = self.hoverImage.get_rect()
                self.hoverImageRect.topleft = (x, y)

        else:
            self.hoverImage = None

        self.image = pygame.transform.scale(image, (self.image_w * scale, self.image_h * scale))
        
        self.imageRect = self.image.get_rect()
        self.imageRect.topleft = (x,y)



    def draw(self, screen, inputs) -> int:
        """
        return 1 if pressed
        """

        pos = pygame.mouse.get_pos()

        if self.imageRect.collidepoint(pos):
            if self.hoverImage != None:
                screen.blit(self.hoverImage, (self.hoverImageRect.x, self.hoverImageRect.y))
            else:
                screen.blit(self.image, (self.imageRect.x, self.imageRect.y))
            if inputs["click"] == True:
                return 1
        else:
            screen.blit(self.image, (self.imageRect.x, self.imageRect.y))