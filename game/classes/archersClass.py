import pygame
import os
from classes.spriteLoader import SpriteLoader
from classes.entityClass import Entity
from classes.projectileClass import Projectile

class Archers():
    def __init__(self, projectileGroup: pygame.sprite.Group, enemies: list) -> None:
        #intialise variables
        self.level = 1
        self.animationFrame = 0
        self.damageValue = 1
        self.upgradePrice = 10
        self.amount = 1
        self.projectileGroup = projectileGroup
        self.enemies = enemies
        
        #load required assets
        self.loadImages()

        #intialise sprite group
        self.archerGroup = pygame.sprite.Group()

    def update(self, dt: float, fps: int) -> None:
        self.archerGroup.update(dt,fps)

    def render(self, screen: pygame.Surface) -> None:
        self.archerGroup.draw(screen)

    def levelUp(self) -> None:
        #levels up to 75
        if self.level < 75:
            if self.amount < 4:
                #adds archers up to 3
                archer = Archer(self.amount, self.lolaSprites, self.lolaMeta, self.arrowImage, self.projectileGroup, self.enemies)
                self.archerGroup.add(archer)
                self.amount += 1
            else:
                #upgrades all of the archers
                for i in self.archerGroup:
                    i.upgrade()
            
            self.level += 1

            #increases upgrade price
            if self.level % 3 == 0:
                self.upgradePrice += 10
                
    def getUpgradePrice(self) -> int:
        return self.upgradePrice
    
    def getLevel(self) -> int:
        return self.level

    def loadImages(self) -> None:
        #loads required assets
        self.lolaSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/lola bunny.png')
        self.lolaMeta = os.getcwd() + '/assets/characters/lola bunny meta.json'
        lolaSpritesObject = SpriteLoader(self.lolaMeta, self.lolaSpriteSheet)
        self.lolaSprites = lolaSpritesObject.getSpritesList()

        self.arrowImage = pygame.image.load(os.getcwd() + '/assets/main game/arrow.png')
        self.arrowImage = pygame.transform.scale_by(self.arrowImage, 2)

    def reset(self) -> None:
        #resets all archers
        for i in self.archerGroup:
            i.animationFrame = 0
            i.lastUpdate = 10

class Archer(Entity, pygame.sprite.Sprite):
    def __init__(self, pos: int, sprites: list, spriteMeta: dict, arrowImage: pygame.Surface, projectileGroup: pygame.sprite.Group, enemiesList: list) -> None:
        #intialise entity parent class
        stats = {'damage':0.25, 'attackSpeed':1, 'arrowSpeed':10}
        Entity.__init__(self, stats, sprites, spriteMeta)

        #intialise sprite
        pygame.sprite.Sprite.__init__(self)

        #set rect1
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()

        #intialise variables
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

    def update(self, dt: float, fps: int) -> None:
        self.animate(0,3,dt,1/(self.stats['attackSpeed']*4))

        #handles shooting
        if self.animationFrame == 3 and not self.shot:
            self.shoot()
            self.shot = True
        elif self.animationFrame != 3 and self.shot:
            self.shot = False

    def shoot(self) -> None:
        #checks if any enemies are present
        if self.enemies.sprites():
            #create a projectile aimed at first enemy created
            target = self.enemies.sprites()[0]
            arrow = Projectile(self.rect.x, self.rect.y, target.rect.center[0], target.rect.center[1], target.stats['runSpeed'], target.stopx, self.arrowImage, self.stats['damage'])
            self.projectilesGroup.add(arrow)

    def upgrade(self) -> None:
        #increase stats
        self.stats['damage'] *= 1.05
        self.stats['attackSpeed'] *= 1.025

    