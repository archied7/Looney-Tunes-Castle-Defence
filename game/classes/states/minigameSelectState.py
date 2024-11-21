from classes.states.tweetyPieState import TweetyPie
from classes.states.roadRunnerState import RoadRunner
from classes.states.stateClass import State
from classes.buttonClass import Button
from classes.states.pauseState import Pause
import pygame
import os

class MinigameSelect(State):
    def __init__(self, main):
        """
        self.status = 0 if minigame is not loaded
        self.status = 1 if minigame is loaded
        """
        State.__init__(self, main)
        self.tweetyMinigameButton = Button(400, 400, self.tweetyMinigameIconImage, 10)
        self.roadRunnerMinigameButton = Button(800,400, self.roadRunnerMinigameIconImage, 2.5)
        self.status = 0

    def update(self, dt, inputs):
        pygame.display.update()
        if self.status == 1:
            self.leaveState()

    def render(self, screen, inputs):
        if inputs['escape'] == True:
            nextState = Pause(self.main)
            nextState.newState()
            
        if self.tweetyMinigameButton.draw(screen, inputs) == 1:
            self.status = 1
            nextState = TweetyPie(self.main)
            nextState.newState()

        if self.roadRunnerMinigameButton.draw(screen, inputs) == 1:
            self.status = 1
            nextState = RoadRunner(self.main)
            nextState.newState()

        


    def loadImages(self):
        self.tweetyMinigameIconImage = pygame.image.load(os.getcwd() + '/assets/misc/tweety game icon.png')
        self.roadRunnerMinigameIconImage = pygame.image.load(os.getcwd() + '/assets/misc/road runner game icon.png')
