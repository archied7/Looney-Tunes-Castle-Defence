import pygame

class Button:
    def __init__(self, x: int, y: int, image: pygame.Surface, scale: float, hoverImage: pygame.Surface = None, hoverType: int = 0) -> None:
        """
        hoverType = 0 if it doesn't grow when hovered over
        hoverType = 1 if it does grow when hovered over
        """
        self.x = x
        self.y = y

        self.image_w = image.get_width()
        self.image_h = image.get_height()
        
        self.scale = scale

        #generates hoverImage
        if hoverImage != None:
            self.hover_w = hoverImage.get_width()
            self.hover_h = hoverImage.get_height()

            #grows the hoverImage if hoverType = 1
            if hoverType == 1:
                self.hoverImage = pygame.transform.scale(hoverImage, (self.hover_w * (scale+0.04), self.hover_h * (scale+0.04)))
                self.hoverImageRect = self.hoverImage.get_rect()
                self.hoverImageRect.topleft = (self.x-4*scale, self.y-4*scale)
            
            #for hoverType = 0
            else:
                self.hoverImage = pygame.transform.scale(hoverImage, (self.hover_w * (scale), self.hover_h * (scale)))
                self.hoverImageRect = self.hoverImage.get_rect()
                self.hoverImageRect.topleft = (self.x, self.y)

        else:
            self.hoverImage = None

        self.image = pygame.transform.scale(image, (self.image_w * scale, self.image_h * scale))
        
        self.imageRect = self.image.get_rect()
        self.imageRect.topleft = (x,y)


    #draws the button and detects if the button is pressed
    def draw(self, screen: pygame.Surface, inputs: dict, invisible: bool=False) -> int:
        """
        return 1 if pressed
        """

        pos = pygame.mouse.get_pos()

        #checks if the mouse is on the button
        if self.imageRect.collidepoint(pos):
            if invisible == False:
                #draws the hover image if there is one
                if self.hoverImage != None:
                    screen.blit(self.hoverImage, (self.hoverImageRect.x, self.hoverImageRect.y))
                else:
                    screen.blit(self.image, (self.imageRect.x, self.imageRect.y))
            if inputs["click"] == True:
                return 1
        #if the mouse is not on the button
        else:
            if invisible == False:
                screen.blit(self.image, (self.imageRect.x, self.imageRect.y))


    #changes the image of the button
    def changeImage(self, image: pygame.Surface, scale: float, hoverImage: pygame.Surface = None, hoverType: int = 0) -> None:
        self.image_w = image.get_width()
        self.image_h = image.get_height()
        
        self.scale = scale

        if hoverImage != None:
            self.hover_w = hoverImage.get_width()
            self.hover_h = hoverImage.get_height()

            if hoverType == 1:
                self.hoverImage = pygame.transform.scale(hoverImage, (self.hover_w * (scale+0.04), self.hover_h * (scale+0.04)))
                self.hoverImageRect = self.hoverImage.get_rect()
                self.hoverImageRect.topleft = (self.x-4*scale, self.y-4*scale)
            
            else:
                self.hoverImage = pygame.transform.scale(hoverImage, (self.hover_w * (scale), self.hover_h * (scale)))
                self.hoverImageRect = self.hoverImage.get_rect()
                self.hoverImageRect.topleft = (self.x, self.y)

        else:
            self.hoverImage = None

        self.image = pygame.transform.scale(image, (self.image_w * scale, self.image_h * scale))
        
        self.imageRect = self.image.get_rect()
        self.imageRect.topleft = (self.x, self.y)