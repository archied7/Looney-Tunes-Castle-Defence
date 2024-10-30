import pygame

class Archers():
    def __init__(self) -> None:
        self.level = 1
        self.animationFrame = 0
        self.damageValue = 1

    def levelUp(self) -> None:
        if self.level < 10:
            self.level += 1
            self.damageValue += 1
        else:
            pass

    def getDamage(self) -> int:
        return self.damageValue

    def shoot():
        pass

