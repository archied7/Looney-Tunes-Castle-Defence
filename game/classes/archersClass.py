import pygame
import os
from classes.spriteLoader import SpriteLoader
from classes.entityClass import Entity
from classes.projectileClass import Projectile

class Archers():
    def __init__(self, projectileGroup, enemies) -> None:
        self.level = 1
        self.animationFrame = 0
        self.damageValue = 1
        self.upgradePrice = 10
        self.amount = 1
        self.projectileGroup = projectileGroup
        self.enemies = enemies
        self.loadImages()

        self.archerGroup = pygame.sprite.Group()

    def update(self, dt, fps):
        self.archerGroup.update(dt,fps)

    def render(self, screen):
        self.archerGroup.draw(screen)

    def levelUp(self) -> None:
        if self.level <= 75:
            if self.amount < 4:
                archer = Archer(self.amount, self.lolaSprites, self.lolaMeta, self.arrowImage, self.projectileGroup, self.enemies)
                self.archerGroup.add(archer)
                self.amount += 1
            else:
                for i in self.archerGroup:
                    i.upgrade()
            
            self.level += 1
            if self.level % 3 == 0:
                self.upgradePrice += 10
                
    def getUpgradePrice(self) -> int:
        return self.upgradePrice
    
    def getLevel(self) -> int:
        return self.level

    def loadImages(self):
        self.lolaSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/lola bunny.png')
        self.lolaMeta = os.getcwd() + '/assets/characters/lola bunny meta.json'
        lolaSpritesObject = SpriteLoader(self.lolaMeta, self.lolaSpriteSheet)
        self.lolaSprites = lolaSpritesObject.getSpritesList()

        self.arrowImage = pygame.image.load(os.getcwd() + '/assets/main game/arrow.png')
        self.arrowImage = pygame.transform.scale_by(self.arrowImage, 2)

    def reset(self):
        for i in self.archerGroup:
            i.animationFrame = 0
            i.lastUpdate = 10

class Archer(Entity, pygame.sprite.Sprite):
    def __init__(self, pos, sprites, spriteMeta, arrowImage, projectileGroup, enemiesList):
        stats = {'damage':0.25, 'attackSpeed':1, 'arrowSpeed':10}
        Entity.__init__(self, stats, sprites, spriteMeta)
        pygame.sprite.Sprite.__init__(self)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.projectilesGroup = projectileGroup
        self.enemies = enemiesList

        if pos == 1:
            self.rect.bottomleft = (130,600)
        elif pos == 2:
            self.rect.bottomleft = (90,600)
        elif pos == 3:
            self.rect.bottomleft = (50, 600)

        self.arrowImage = arrowImage
        self.shot = False

    def update(self, dt, fps):
        self.animate(0,3,dt,1/(self.stats['attackSpeed']*4))
        if self.animationFrame == 3 and not self.shot:
            self.shoot()
            self.shot = True
        elif self.animationFrame != 3 and self.shot:
            self.shot = False

    def shoot(self):
        if self.enemies.sprites():
            target = self.enemies.sprites()[0]
            arrow = Projectile(self.rect.x, self.rect.y, target.rect.x, target.rect.y, target.stats['runSpeed'], target.stopx, self.arrowImage, self.stats['damage'])
            self.projectilesGroup.add(arrow)

    def upgrade(self):
        self.stats['damage'] *= 1.05
        self.stats['attackSpeed'] *= 1.025