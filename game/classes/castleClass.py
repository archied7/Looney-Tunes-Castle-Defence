import pygame

class Castle():
    def __init__(self):
        self.level = 1
        self.maxHealth = 50
        self.currentHealth = 50
        self.upgradePrice = 10
        self.healthMultiplier = 1
        self.alive = True

    def upgrade(self) -> None:
        if self.level <= 75:
            self.level += 1
            self.maxHealth += self.upgradePrice + 10
            self.currentHealth = self.maxHealth
            if self.level % 5 == 0:
                self.upgradePrice += 10

    def takeDamage(self, val) -> None:
        if not self.currentHealth - val < 1:
            self.currentHealth -= val
        else:
            self.alive = False
    
    def reset(self):
        self.alive = True
        self.currentHealth = self.maxHealth
