import pygame

class Castle():
    def __init__(self) -> None:
        #sets initial values
        self.level = 1
        self.maxHealth = 50
        self.currentHealth = 50
        self.upgradePrice = 10
        self.alive = True

    def upgrade(self) -> None:
        #increases stats up to level 75
        if self.level < 75:
            self.level += 1
            self.maxHealth += self.upgradePrice + 10
            self.currentHealth = self.maxHealth

            #increases upgrade price
            if self.level % 5 == 0:
                self.upgradePrice += 10

    def takeDamage(self, val: int) -> None:
        #checks for death and changes health
        if not self.currentHealth - val < 1:
            self.currentHealth -= val
        else:
            self.alive = False
    
    def reset(self):
        #resets variables
        self.alive = True
        self.currentHealth = self.maxHealth

