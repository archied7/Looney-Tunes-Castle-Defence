import pygame


class Entity():
    def __init__(self, stats: dict, position: pygame.Vector2) -> None:
        self.stats = stats
        self.animationFrame = 0
        self.position = position

    def projectileAttack(self) -> None:
        pass

    def physicalAttack(self) -> None:
        pass
        