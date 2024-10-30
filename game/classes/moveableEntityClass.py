from entityClass import Entity
import pygame

class Moveable_Entity(Entity):
    def __init__(self, stats: dict, position: pygame.Vector2, enemy: bool) -> None:
        super().__init__(stats, position)
        self.isEnemy = enemy

    def move():
        pass