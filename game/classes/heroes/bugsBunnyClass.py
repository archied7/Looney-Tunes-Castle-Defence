from classes.heroes.heroClass import Hero
from classes.entityClass import Entity
import pygame

class BugsBunny(Hero):
    def __init__(self, spriteList, spriteMeta) -> None:
        stats = {"maxCooldown" : 3, "currentCooldown" : 3, "damage": 1, "attackSpeed" : 1, "abilityValue": 1}
        
        self.goonSpriteMeta = spriteMeta
        Hero.__init__(self, stats, spriteList, spriteMeta)
        self.intermissionImage = self.sprites[0]

        self.goonGroup = pygame.sprite.Group()

        self.name = 'bugsBunny'


    def update(self, dt, fps, inputs):
        if self.abilityInUse:
            if self.animationFrame != 2:
                self.animate(1,2, dt)
            else:
                self.animationFrame = 0
                self.abilityInUse = False
        else:
            self.image = self.sprites[self.animationFrame]

        if self.stats['currentCooldown'] < self.stats['maxCooldown']:
            self.stats['currentCooldown'] += 0.1
        

        self.goonGroup.update(dt, fps)

    def render(self, screen, x, y):
        screen.blit(self.image, (x, y))
        self.drawBar(screen, 1, self.stats['maxCooldown'], self.stats['currentCooldown'], x, y)

        self.goonGroup.draw(screen)

    def useAbility(self):
        if self.stats['currentCooldown'] >= self.stats['maxCooldown']:
            self.abilityInUse = True
            self.stats['currentCooldown'] = 0

            goon = BugsBunnyGoon(self.stats["damage"], self.sprites, 1, self.goonSpriteMeta, self.stats["abilityValue"])
            self.goonGroup.add(goon)
            goon = BugsBunnyGoon(self.stats["damage"], self.sprites, 2, self.goonSpriteMeta, self.stats["abilityValue"])
            self.goonGroup.add(goon)
            goon = BugsBunnyGoon(self.stats["damage"], self.sprites, 3, self.goonSpriteMeta, self.stats["abilityValue"])
            self.goonGroup.add(goon)

    def reset(self):
        super().reset()
        for i in self.goonGroup:
            i.kill()


class BugsBunnyGoon(pygame.sprite.Sprite, Entity):
    def __init__(self, damage, sprites, row, spritesMeta, abilityValue):
        pygame.sprite.Sprite.__init__(self)

        stats = {"damage": damage, "runSpeed": 15}
        Entity.__init__(self, stats, sprites, spritesMeta)
        self.animationFrame = 3
        self.image = self.sprites[self.animationFrame]

        self.currentDamage = stats['damage']
        self.initalDamage = stats["damage"]

        self.x = 750

        self.rect = self.image.get_rect()
        if row == 1:
            self.rect.bottomleft = (self.x, 700)
        elif row == 2:
            self.rect.bottomleft = (self.x, 600)
        elif row == 3:
            self.rect.bottomleft = (self.x, 500)


    def update(self, dt, fps):
        self.animate(3,5, dt, 0.1)
        self.rect.x += self.stats["runSpeed"] * dt * fps + self.xOffset
        if self.rect.left > 1440:
            self.kill()

    def takeDamage(self, val):
        if self.stats['damage'] >= val:
            self.currentDamage = self.stats['damage']
            self.stats['damage'] -= val
        else:
            self.kill()




        