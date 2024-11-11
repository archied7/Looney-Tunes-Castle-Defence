from classes.states.stateClass import State
import pygame
import os

class MainGame(State):
    def __init__(self, main) -> None:
        State.__init__(self, main)

    def update(self, dt) -> None:
        pygame.display.update()

    def render(self, screen) -> None:
        screen.fill((0,0,0))
        screen.blit(self.backgroundImage, (0,0))

    #loads images required for the main game
    def loadImages(self) -> None:
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/main game/main background.png')