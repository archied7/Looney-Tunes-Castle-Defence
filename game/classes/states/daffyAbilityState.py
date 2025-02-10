from classes.states.stateClass import State
from classes.projectileClass import Bullet
import pygame

class daffyAbility(State):
    def __init__(self, main: object, damage: float, image: pygame.Surface):
        #initialise parent class
        State.__init__(self, main)

        self.damage = damage
        self.image = image

        #create semi transparent surface
        self.surface = pygame.Surface((1440,900), pygame.SRCALPHA)
        self.surface.fill((0,0,0,100))
        self.grayed = False

        self.x = 770
        self.width1 = 0
        self.width2 = 630

    def update(self, dt: float, inputs: dict) -> None:
        pygame.display.update()

        #updates current position
        self.x = pygame.mouse.get_pos()[0]
        if self.x <= 770:
            self.x = 770
        elif self.x >= 1300:
            self.x = 1300

        self.width1 = self.x - 770
        self.width2 = 1340 - self.x

        #creates projectile
        if inputs['click']:
            bullet = Bullet(self.image, self.x, 900, self.damage, False, self.x, 0)
            self.main.game.projectileGroup.add(bullet)
            self.leaveState()


    def render(self, screen: pygame.Surface, inputs: dict) -> None:
        #handles graying the screen
        if self.grayed is not True:
            screen.blit(self.surface, (0,0))
            self.grayed = True

        #draws white to the left of the choice
        pygame.draw.rect(screen, (255,255,255), (770, 800, self.width1, 2))
        #draws white to the right of the choice
        pygame.draw.rect(screen, (255,255,255), (1340-self.width2, 800, self.width2, 2))
        #draws black of the choice
        pygame.draw.rect(screen, (0, 0, 0), (self.x, 800, 40, 2))