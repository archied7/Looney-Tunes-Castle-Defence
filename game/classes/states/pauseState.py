from classes.states.stateClass import State
from classes.buttonClass import Button
import pygame
import os

class Pause(State):
    def __init__(self, main) -> None:
        State.__init__(self, main)
        self.exitButton = Button(539, 450, self.main.exitImage, 2.5, self.main.exitHoverImage)
        self.pauseButton = Button(539, 300, self.pauseImage, 2.5, self.pauseHoverImage)

    def update(self, dt, inputs) -> None:
        pygame.display.update()

    def render(self, screen, inputs) -> None:
        if self.pauseButton.draw(screen, inputs) == 1 :
            self.leaveState()

        if self.exitButton.draw(screen, inputs) == 1:
            self.main.running = False


    def loadImages(self) -> None:
        self.pauseImage = pygame.image.load(os.getcwd() + '/assets/misc/pause.png')
        self.pauseHoverImage = pygame.image.load(os.getcwd() + '/assets/misc/pause hover.png')