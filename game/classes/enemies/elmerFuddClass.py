from classes.enemies.enemyClass import Enemy
from classes.projectileClass import Bullet
import pygame

class ElmerFudd(Enemy, pygame.sprite.Sprite):
    def __init__(self, sprites, spritesMeta, y, castle, multiplier, projectileGroup):
        pygame.sprite.Sprite.__init__(self)
        stats = {"maxHealth": 4 * multiplier, "currentHealth": 4 * multiplier, "damage": 1 * multiplier, "attackSpeed": 1, "runSpeed": 3, "value": 10}
        Enemy.__init__(self, stats, sprites, spritesMeta, y, castle)
        self.projectileGroup = projectileGroup
        self.bulletSprites = [self.sprites[4]]
        self.stopx = 1100


    def update(self, dt, fps):
        if self.rect.x > self.stopx:
            self.animate(0,2,dt)
            self.rect.x -= self.stats['runSpeed'] * dt * fps
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
        bullet = Bullet(self.bulletSprites, self.rect.x, self.rect.y+53, self.stats['damage'],True)
        self.projectileGroup.add(bullet)

    