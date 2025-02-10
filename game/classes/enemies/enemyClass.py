from classes.entityClass import Entity
import pygame

class Enemy(Entity):
    def __init__(self, stats: dict, sprites: list, spritesMeta: dict, y: int, castle: object) -> None:
        #initialises parent class
        Entity.__init__(self, stats, sprites, spritesMeta)

        #initialises variables
        self.alive = True
        self.castle = castle

        #initialises rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (1350, y)

    def takeDamage(self, value: int) -> None:
        #takes damage away from current health
        self.stats['currentHealth'] -= value

        #checks for enemy's death
        if self.stats['currentHealth'] <= 0:
            self.alive = False
            self.kill()

    #abstract function for update
    def update(self, dt: float, fps: int) -> None:
        pass

    #abstract function for drawing the enemy
    def draw(self, screen: pygame.Surface) -> None:
        pass

    

    

    