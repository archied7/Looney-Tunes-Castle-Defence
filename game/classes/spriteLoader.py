import pygame
import json

class SpriteLoader():
    def __init__(self, metaDir: str, spriteSheet: pygame.Surface, minigameSprite: bool = False) -> None:
        #sets the scale for each sprite, dependant on if it is for a minigame
        if minigameSprite:
            self.scale = 5
        else:
            self.scale = 2

        #adds sprites to a dictionary
        self.sprites = {}
        f = open(metaDir)
        self.data = json.load(f)
        for i in self.data['frames'].items():
            currentSpriteName = i[0]
            i = i[1]['frame']
            currentSprite = self.loadSprites(spriteSheet, i['x'], i['y'], i['width'], i['height'])
            self.sprites[currentSpriteName] = currentSprite


    def loadSprites(self, spriteSheet: pygame.Surface, x: int, y: int, width: int, height: int) -> pygame.Surface:
        #creates sprite
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(spriteSheet,(0,0), (x, y, width,  height))
        sprite = pygame.transform.scale(sprite, (width*self.scale, height*self.scale))
        return sprite

    def getSpritesList(self):
        #returns the sprites in a list
        sprites = []
        for i in self.sprites:
            sprites.append(self.sprites[i])
        return sprites


    