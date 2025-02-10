from classes.heroes.heroClass import Hero
import pygame

class DaffyDuck(Hero):
    def __init__(self, spriteList: list, spriteMeta: list, arrowImage: pygame.Surface) -> None:
        stats = {"maxCooldown": 20, "currentCooldown": 20, "damage": 1, "attackSpeed": 1, "abilityValue": 1}
        Hero.__init__(self, stats, spriteList, spriteMeta)
        self.intermissionImage = self.sprites[0]
        self.arrowImage = [arrowImage]

        self.name = 'daffyDuck'

    def update(self, dt: float, fps: int, inputs: dict) -> None:
        self.animate(0, 1, dt)

        #updates cooldown
        if self.stats['currentCooldown'] < self.stats['maxCooldown']:
            self.stats['currentCooldown'] += 0.1

    def render(self, screen: pygame.Surface, x: int, y: int) -> None:
        screen.blit(self.image, (x+self.xOffset, y+self.yOffset+20))
        self.drawBar(screen, 1, self.stats['maxCooldown'], self.stats['currentCooldown'], x, y)

    def useAbility(self):
        if self.stats['currentCooldown'] >= self.stats['maxCooldown']:
            self.stats['currentCooldown'] = 0
            self.abilityInUse = True

    