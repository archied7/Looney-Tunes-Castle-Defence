import pygame


class Entity():
    def __init__(self, stats: dict, position: pygame.Vector2, sprites: dict) -> None:
        self.stats = stats
        self.animationFrame = 0
        self.position = position
        self.sprites = list(self.sprites.values())
        self.currentSprite = None

    def projectileAttack(self) -> None:
        pass

    def physicalAttack(self) -> None:
        pass
        
    def animate(self, rangeStart, rangeEnd) -> None:
        self.animationFrame = rangeStart
        if self.animationFrame < rangeEnd:
            self.currentSprite = self.sprites[self.animationFrame]
            self.animationFrame += 1
        else:
            self.currentSprite = self.sprites[rangeStart]
            self.animationFrame = rangeStart