import pygame
import json


class Entity():
    def __init__(self, stats: dict, sprites: list, spritesMeta: dict) -> None:
        self.stats = stats
        self.animationFrame = 0
        self.sprites = sprites

        self.spritesMeta = []
        f = open(spritesMeta)
        self.data = json.load(f)
        for i in self.data['frames'].items():
            self.spritesMeta.append([i[1]['frame']['width'], i[1]['frame']['height']])
            
        self.image = sprites[0]
        self.lastUpdate = 10
        self.set = False
        self.xOffset = 0
        self.yOffset = 0
        self.shot = False


    def projectileAttack(self) -> None:
        pass

    def physicalAttack(self) -> None:
        pass
        
    def animate(self, rangeStart, rangeEnd, dt, speed=0.15) -> None:
        self.lastUpdate += dt

        if self.lastUpdate > speed:
            self.lastUpdate = 0  # Reset the update interval

            # Increment the animation frame
            self.animationFrame += 1

            # Reset the frame to rangeStart if it exceeds rangeEnd
            if self.animationFrame > rangeEnd:
                self.animationFrame = rangeStart

            # Update the current sprite image and offsets
            self.image = self.sprites[self.animationFrame]
            self.xOffset = self.spritesMeta[0][0] - self.spritesMeta[self.animationFrame][0]
            self.yOffset = self.spritesMeta[0][1] - self.spritesMeta[self.animationFrame][1]


    def drawBar(self, screen, type, maxVal, currentVal, x, y):
        """
        type = 0 for enemies
        type = 1 for heroes
        """

        fill = (currentVal / maxVal) * 50
        if type == 0:
            pygame.draw.rect(screen, (255,255,255), (x,y,50,10))
            pygame.draw.rect(screen, (120, 6, 6), (x,y,fill , 10))

        if type == 1:
            pygame.draw.rect(screen, (255,255,255), (x,y,50,7))
            pygame.draw.rect(screen, (173, 216, 230), (x,y,fill,7))




