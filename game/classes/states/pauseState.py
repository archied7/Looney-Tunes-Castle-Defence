from classes.states.stateClass import State
from classes.buttonClass import Button
import pygame
import os

class Pause(State):
    def __init__(self, main: object) -> None:
        #initialises parent class
        State.__init__(self, main)

        #creates buttons
        self.exitButton = Button(539, 450, self.main.exitImage, 2.5, self.main.exitHoverImage)
        self.pauseButton = Button(539, 300, self.pauseImage, 2.5, self.pauseHoverImage)

        #create semi transparent surface
        self.surface = pygame.Surface((1440,900), pygame.SRCALPHA)
        self.surface.fill((0,0,0,100))

        self.grayed = False
        self.main.game.changePause()

    def update(self, dt: float, inputs: dict) -> None:
        pygame.display.update()

    def render(self, screen: pygame.Surface, inputs: dict) -> None:
        #handles graying the screen
        if self.grayed is not True:
            screen.blit(self.surface, (0,0))
            self.grayed = True

        #checks if pause button pressed
        if self.pauseButton.draw(screen, inputs) == 1:
            self.leaveState()

        #checks if exit button pressed
        if self.exitButton.draw(screen, inputs) == 1:
            self.main.saveLoadManager.save()
            self.main.running = False


    def loadImages(self) -> None:
        self.pauseImage = pygame.image.load(os.getcwd() + '/assets/misc/pause.png')
        self.pauseHoverImage = pygame.image.load(os.getcwd() + '/assets/misc/pause hover.png')