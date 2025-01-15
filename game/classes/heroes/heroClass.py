from classes.entityClass import Entity
import pygame

class Hero(Entity):
    """
        self.stats = {"maxCooldown": float
                     "currentCooldown" : float
                     "damage": int
                     "attackSpeed": int}
    """
    def __init__(self, stats: dict, spriteList: list, spriteMeta: dict) -> None:
        super().__init__(stats, spriteList, spriteMeta)
        self.upgradePrice = 10
        self.level = 1
        self.abilityInUse = False
        
    def attack(self):
        super().projectileAttack()
    
    def levelUp(self) -> None:
        if self.level <= 9:
            self.level += 1
            self.stats["attackSpeed"] *= 1.1
            self.stats["damage"] *= 1.05
            self.stats["abilityValue"] *= 1.1
            self.stats['maxCooldown'] -= 0.15
            if self.level == 10:
                self.upgradePrice = 'MAX'
            else:
                if self.level == 2:
                    self.upgradePrice += 40
                else:
                    self.upgradePrice += 50

    def useAbility(self) -> None:
        pass

    def reset(self) -> None:
        self.stats['currentCooldown'] = self.stats['maxCooldown']
        self.animationFrame = 0
        self.image = self.sprites[self.animationFrame]
 