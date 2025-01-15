from classes.heroes.heroClass import Hero
from classes.projectileClass import Bullet
import pygame

class YosemiteSam(Hero):
    def __init__(self, spriteList, spriteMeta, projectileGroup, enemyGroup):
        stats = {"maxCooldown": 20, "currentCooldown": 20, "damage": 1, "attackSpeed": 1, "abilityValue": 3}
        Hero.__init__(self, stats, spriteList, spriteMeta)
        self.intermissionImage = self.sprites[0]
        self.lastUpdateAbility = 0
        self.attackSpeed = self.stats["attackSpeed"]
        self.projectileGroup = projectileGroup
        self.enemyGroup = enemyGroup
        self.x, self.y = 0,0
        self.bulletSprites = [self.sprites[8], self.sprites[9]]

        self.name = 'yosemiteSam'

    def update(self, dt, fps, inputs):
        if self.abilityInUse:
            self.animate(4, 7, dt, 1/30)
            self.lastUpdateAbility += dt
            if self.lastUpdateAbility > self.stats["abilityValue"]:
                self.lastUpdateAbility = dt
                self.abilityInUse = False
            if self.animationFrame == 7 and not self.shot:
                self.shoot()
                self.shot = True
            elif self.animationFrame == 4 and self.shot:
                self.shot = False

        else:
            self.animate(0, 3, dt, 1/(self.stats["attackSpeed"]*3))
            if self.animationFrame == 3 and not self.shot:
                self.shoot()
                self.shot = True
            elif self.animationFrame == 0 and self.shot:
                self.shot = False

        if self.stats['currentCooldown'] < self.stats['maxCooldown']:
            self.stats['currentCooldown'] += 0.1

    def render(self, screen, x, y):
        self.x = x
        self.y = y
        screen.blit(self.image, (x+self.xOffset, y+self.yOffset+27))
        self.drawBar(screen, 1, self.stats['maxCooldown'], self.stats['currentCooldown'], x, y)

    def useAbility(self):
        if self.stats['currentCooldown'] >= self.stats['maxCooldown']:
            self.stats['currentCooldown'] = 0
            self.abilityInUse = True

    def shoot(self):
        if self.enemyGroup:
            target = self.enemyGroup.sprites()[0]
            bullet = Bullet(self.bulletSprites, self.x+40, self.y+50, self.stats['damage'], False, target.rect.topleft[0], target.rect.center[1], True)
            self.projectileGroup.add(bullet)
            

    