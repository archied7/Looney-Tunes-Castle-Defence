from classes.entityClass import Entity
import pygame

class Enemy(Entity):
    def __init__(self, stats: dict, sprites: list, spritesMeta: dict, y: int, castle: object) -> None:
        Entity.__init__(self, stats, sprites, spritesMeta)
        self.alive = True
        self.rect = self.image.get_rect()
        self.rect.topleft = (1350, y)
        self.castle = castle

    def takeDamage(self, value):
        self.stats['currentHealth'] -= value
        if self.stats['currentHealth'] <= 0:
            self.alive = False
            self.kill()

    def update(self, dt, fps):
        pass

    def draw(self, screen):
        pass

    

    

    