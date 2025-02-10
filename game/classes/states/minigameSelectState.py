from classes.states.tweetyPieState import TweetyPie
from classes.states.roadRunnerState import RoadRunner
from classes.states.stateClass import State
from classes.buttonClass import Button
from classes.states.pauseState import Pause
import pygame
import os

class MinigameSelect(State):
    def __init__(self, main: object) -> None:
        """
        self.status = 0 if minigame is not loaded
        self.status = 1 if minigame is loaded
        """
        #initialise parent class
        State.__init__(self, main)

        #create buttons
        self.tweetyMinigameButton = Button(400, 300, self.tweetyMinigameIconImage, 10)
        self.roadRunnerMinigameButton = Button(800,300, self.roadRunnerMinigameIconImage, 2.5)

        #set variables
        self.status = 0
        self.lived = self.main.survivedRound
        self.main.survivedRound = True

        #create semi transparent surface
        self.surface = pygame.Surface((1440,900), pygame.SRCALPHA)
        if self.lived:
            self.surface.fill((0,0,0,100))
        else:
            self.surface.fill((120,6,6,200))

        self.grayed = False
        
    def update(self, dt: float, inputs: dict) -> None:
        pygame.display.update()

        #leave state after minigame is complete
        if self.status == 1:
            self.leaveState()

    def render(self, screen: pygame.Surface, inputs: dict) -> None:
        #handles pausing
        if inputs['escape'] == True:
            nextState = Pause(self.main)
            nextState.newState()

        #handles drawing semi transparent surface
        if self.grayed is not True:
            screen.blit(self.surface, (0,0))
            self.grayed = True

        #draws background image
        screen.blit(self.backgroundImage, (355, 254))
        self.main.drawText('Reward: ' + str(self.main.minigameValue) + 'G', 614, 650, 30)
            
        #draws buttons
        if self.tweetyMinigameButton.draw(screen, inputs) == 1:
            self.status = 1
            nextState = TweetyPie(self.main)
            nextState.newState()

        if self.roadRunnerMinigameButton.draw(screen, inputs) == 1:
            self.status = 1
            nextState = RoadRunner(self.main)
            nextState.newState()

    def loadImages(self) -> None:
        #loads images
        self.tweetyMinigameIconImage = pygame.image.load(os.getcwd() + '/assets/misc/tweety game icon.png')
        self.roadRunnerMinigameIconImage = pygame.image.load(os.getcwd() + '/assets/misc/road runner game icon.png')
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/misc/minigame background.png')
