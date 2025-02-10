from classes.enemies.enemyClass import Enemy
from classes.projectileClass import Bullet
import pygame

class MarvinMartian(Enemy, pygame.sprite.Sprite):
    def __init__(self, sprites: list, spritesMeta: dict, y: int, castle: object, multiplier: float, projectileGroup: pygame.sprite.Group) -> None:
        #initialise sprite
        pygame.sprite.Sprite.__init__(self)

        #initialise Enemy parent class
        stats = {"maxHealth": 13 * multiplier, "currentHealth": 13 * multiplier, "damage": 10 * multiplier, "attackSpeed": 1, "runSpeed": 1, "value": 15}
        Enemy.__init__(self, stats, sprites, spritesMeta, y, castle)

        #set variables
        self.animationFrame = 2
        self.projectileGroup = projectileGroup
        self.bulletSprites = [self.sprites[2], self.sprites[3]]
        self.stopx = 825

    def update(self, dt: float, fps: int) -> None:
        #movement
        if self.rect.x > self.stopx:
            self.rect.x -= self.stats['runSpeed'] * dt * fps    
        self.animate(0,1, dt)

        #shooting
        if self.animationFrame == 1 and self.rect.x <= self.stopx and not self.shot:
            self.shoot()
            self.shot = True
        elif self.animationFrame == 0 and self.shot:
            self.shot = False

    def draw(self, screen: pygame.Surface) -> None:
        #draws current frame
        screen.blit(self.image, (self.rect.x + self.xOffset, self.rect.y + self.yOffset))
        #draw health bar
        self.drawBar(screen, 0, self.stats['maxHealth'], self.stats['currentHealth'], self.rect.x, self.rect.y-10)

    def shoot(self):
        #creates bullet object
        bullet = Bullet(self.bulletSprites, self.rect.x, self.rect.y+45, self.stats['damage'], True, None, None, True)
        #adds to the sprite group
        self.projectileGroup.add(bullet)
        