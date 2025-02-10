import pygame
import json


class Entity():
    def __init__(self, stats: dict, sprites: list, spritesMeta: str) -> None:
        self.stats = stats
        self.animationFrame = 0
        self.sprites = sprites

        #creates a list containing the sprite meta data used for calculating offsets
        self.spritesMeta = []
        f = open(spritesMeta)
        self.data = json.load(f)
        for i in self.data['frames'].items():
            self.spritesMeta.append([i[1]['frame']['width'], i[1]['frame']['height']])
            
        #sets variables
        self.image = sprites[0]
        self.lastUpdate = 10
        self.xOffset = 0
        self.yOffset = 0
        self.shot = False

    def animate(self, rangeStart: int, rangeEnd: int, dt: float, speed: float=0.15) -> None:
        self.lastUpdate += dt

        if self.lastUpdate > speed:
            #resets the update interval
            self.lastUpdate = 0 

            #increments the animation frame
            self.animationFrame += 1

            #resets the frame to rangeStart if it exceeds rangeEnd
            if self.animationFrame > rangeEnd:
                self.animationFrame = rangeStart

            #updates the current sprite image and offsets
            self.image = self.sprites[self.animationFrame]
            self.xOffset = self.spritesMeta[0][0] - self.spritesMeta[self.animationFrame][0]
            self.yOffset = self.spritesMeta[0][1] - self.spritesMeta[self.animationFrame][1]


    #draws ability cooldown and health bars
    def drawBar(self, screen: pygame.Surface, type: int, maxVal: float, currentVal: float, x: int, y: int) -> None:
        """
        type = 0 for enemies
        type = 1 for heroes
        """

        #calculates the amount the bar will be full
        fill = (currentVal / maxVal) * 50

        if type == 0:
            #draws full bar
            pygame.draw.rect(screen, (255,255,255), (x,y,50,10))
            #draws the amount the bar is full
            pygame.draw.rect(screen, (120, 6, 6), (x,y,fill , 10))

        if type == 1:
            #draws full bar
            pygame.draw.rect(screen, (255,255,255), (x,y,50,7))
            #draws the amount the bar is full
            pygame.draw.rect(screen, (173, 216, 230), (x,y,fill,7))




