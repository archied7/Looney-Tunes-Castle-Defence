from classes.enemies.enemyClass import Enemy
from classes.projectileClass import Bullet
import pygame

class ElmerFudd(Enemy, pygame.sprite.Sprite):
    def __init__(self, sprites: list, spritesMeta: dict, y: int, castle: object, multiplier: float, projectileGroup: pygame.sprite.Group) -> None:
        #initalise sprite
        pygame.sprite.Sprite.__init__(self)

        #initialise enemy parent class
        stats = {"maxHealth": 4 * multiplier, "currentHealth": 4 * multiplier, "damage": 1 * multiplier, "attackSpeed": 1, "runSpeed": 3, "value": 10}
        Enemy.__init__(self, stats, sprites, spritesMeta, y, castle)

        #initalise variables
        self.projectileGroup = projectileGroup
        self.bulletSprites = [self.sprites[4]]
        self.stopx = 1100


    def update(self, dt: float, fps: int):
        #movement
        if self.rect.x > self.stopx:
            self.animate(0,2,dt)
            self.rect.x -= self.stats['runSpeed'] * dt * fps
        #attacking
        else:
            self.animate(2,3, dt, 0.2)
            if self.animationFrame == 3 and not self.shot:
                self.shoot()
                self.shot = True
            elif self.animationFrame == 2 and self.shot:
                self.shot = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x+self.xOffset, self.rect.y))
        self.drawBar(screen, 0, self.stats['maxHealth'], self.stats['currentHealth'], self.rect.x, self.rect.y - 10)
        
    def shoot(self):
        #creates bullet
        bullet = Bullet(self.bulletSprites, self.rect.x, self.rect.y+53, self.stats['damage'],True)

        #adds bullet to projectile group
        self.projectileGroup.add(bullet)

    