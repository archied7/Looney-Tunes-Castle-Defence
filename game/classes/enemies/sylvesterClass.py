from classes.enemies.enemyClass import Enemy
import pygame

class Sylvester(Enemy, pygame.sprite.Sprite):
    def __init__(self, sprites: list, spritesMeta: dict, y: int, castle: object, multiplier: float) -> None:
        #adjusts y variable for the sprites
        y = y+10

        #initialises sprite
        pygame.sprite.Sprite.__init__(self)

        #initialises Enemy parent class
        stats = {"maxHealth": 2 * multiplier, "currentHealth": 2 * multiplier, "damage": 5 * multiplier, "attackSpeed": 1, "runSpeed": 5, "value": 5}
        Enemy.__init__(self, stats, sprites, spritesMeta, y, castle)

        #sets variables
        self.attackCooldown = self.stats['attackSpeed']
        self.stopx = 775

    def update(self, dt: float, fps: int) -> None:
        #during movement
        if self.rect.x > self.stopx:
            self.animate(1,5,dt)
            self.rect.x -= self.stats['runSpeed'] * dt * fps

        #during attacking
        else:
            self.animationFrame = 0
            self.image = self.sprites[self.animationFrame]
            self.attackCooldown -= dt

            if self.attackCooldown <= 0:
                self.castle.takeDamage(self.stats['damage'])
                self.attackCooldown = self.stats['attackSpeed']

    def draw(self, screen: pygame.Surface) -> None:
        #draw enemy
        screen.blit(self.image, (self.rect.x + self.xOffset, self.rect.y + self.yOffset))

        #draw health bar
        self.drawBar(screen, 0, self.stats['maxHealth'], self.stats['currentHealth'], self.rect.x, self.rect.y-10)

