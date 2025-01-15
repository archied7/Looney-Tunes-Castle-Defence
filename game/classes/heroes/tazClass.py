from classes.heroes.heroClass import Hero
from classes.projectileClass import Projectile
import pygame

class Taz(Hero):
    def __init__(self, spriteList, spriteMeta, projectileGroup, enemyGroup):
        stats = {"maxCooldown": 10, "currentCooldown": 10, "damage": 1, "attackSpeed": 1, "abilityValue": 1}
        Hero.__init__(self, stats, spriteList, spriteMeta)
        self.intermissionImage = self.sprites[0]
        self.animationFrame = 0
        self.projectileGroup = projectileGroup
        self.enemyGroup = enemyGroup
        self.x = -100
        self.y = -100

        self.name = 'taz'

    def update(self, dt, fps, inputs):
        if self.abilityInUse:
            if self.animationFrame != 10:
                self.animate(2, 10, dt)
                if self.animationFrame % 2 == 0 and not self.shot:
                    self.shoot()
                    self.shot = True
                elif self.animationFrame % 2 != 0 and self.shot:
                    self.shot = False
            else:
                self.animationFrame = 0
                self.image = self.sprites[self.animationFrame]
                self.abilityInUse = False
        else:
            self.animate(0,1, dt, 1/self.stats['attackSpeed'])
            if self.animationFrame == 0 and not self.shot:
                self.shoot()
                self.shot = True
            elif self.animationFrame == 1 and self.shot:
                self.shot = False

        if self.stats['currentCooldown'] < self.stats['maxCooldown']:
            self.stats['currentCooldown'] += 0.1

            

    def render(self, screen, x, y):
        self.x = x
        self.y = y
        screen.blit(self.image, (x+self.xOffset, y+self.yOffset+15))
        self.drawBar(screen, 1, self.stats['maxCooldown'], self.stats['currentCooldown'], x, y)

    def levelUp(self):
        return super().levelUp()

    def useAbility(self):
        if self.stats['currentCooldown'] >= self.stats['maxCooldown']:
            self.stats['currentCooldown'] = 0
            self.abilityInUse = True

    def shoot(self):
        if self.enemyGroup.sprites():
            target = self.enemyGroup.sprites()[0]
            meat = Projectile(self.x, self.y, target.rect.x, target.rect.y, target.stats['runSpeed'], target.stopx, self.sprites[10], self.stats['damage'])
            self.projectileGroup.add(meat)
    