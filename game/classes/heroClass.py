from entityClass import Entity
import pygame

class Hero(Entity):
    """
        self.stats = {"attackSpeed": float
                     "
                     "damage": int
                     "maxCooldown": int 
                     "currentCooldown": int}
    """
    def __init__(self, stats: dict, position: pygame.Vector2) -> None:
        super().__init__(stats, position)
        self.stats.append("currentCooldown", 0)
        
        self.level = 1
        
    def attack(self):
        super().projectileAttack()
    
    def levelUp(self) -> None:
        if self.level <= 10:
            pass
        else:
            self.level += 1
            self.stats["maxHealth"] = self.stats["maxHealth"] * 1.1

    def useAbility(self) -> None:
        pass
 