import pygame
import json

class SpriteLoader():
    def __init__(self, metaDir, spriteSheet) -> None:
        self.scale = 5
        self.sprites = {}
        f = open(metaDir)
        self.data = json.load(f)
        for i in self.data['frames'].items():
            currentSpriteName = i[0]
            i = i[1]['frame']
            currentSprite = self.loadSprites(spriteSheet, i['x'], i['y'], i['width'], i['height'])
            self.sprites[currentSpriteName] = currentSprite


    def loadSprites(self, spriteSheet, x, y, width, height) -> pygame.Surface:
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(spriteSheet,(0,0), (x, y, width,  height))
        sprite = pygame.transform.scale(sprite, (width*self.scale, height*self.scale))
        return sprite
    
    def getSprites(self):
        return self.sprites

    