from classes.states.stateClass import State
from classes.projectileClass import Bullet
import pygame

class daffyAbility(State):
    def __init__(self, main, damage, image):
        State.__init__(self, main)
        self.damage = damage
        self.image = image

        self.surface = pygame.Surface((1440,900), pygame.SRCALPHA)
        self.surface.fill((0,0,0,100))

        self.grayed = False
        self.x = 770
        self.width1 = 0
        self.width2 = 630

    def update(self, dt, inputs):
        pygame.display.update()

        self.x = pygame.mouse.get_pos()[0]
        if self.x <= 770:
            self.x = 770
        elif self.x >= 1300:
            self.x = 1300

        self.width1 = self.x - 770
        self.width2 = 1340 - self.x

        if inputs['click']:
            bullet = Bullet(self.image, self.x, 900, self.damage, False, self.x, 0)
            self.main.game.projectileGroup.add(bullet)
            self.leaveState()




    def render(self, screen, inputs):
        if self.grayed is not True:
            screen.blit(self.surface, (0,0))
            self.grayed = True

        pygame.draw.rect(screen, (255,255,255), (770, 800, self.width1, 2))
        pygame.draw.rect(screen, (255,255,255), (1340-self.width2, 800, self.width2, 2))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, 800, 40, 2))