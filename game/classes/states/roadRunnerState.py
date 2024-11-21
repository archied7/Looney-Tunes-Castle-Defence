from classes.states.stateClass import State
from classes.spriteLoader import SpriteLoader
from classes.states.pauseState import Pause
from classes.buttonClass import Button
import pygame
import os

class RoadRunner(State):
    def __init__(self, main) -> None:
        State.__init__(self, main)
        self.exitButton = Button(538, 700, self.main.exitImage, 2.5, self.main.exitHoverImage)

    def update(self, dt, inputs) -> None:
        pygame.display.update()

    def render(self, screen, inputs) -> None:
        screen.fill((0,0,0))
        screen.blit(self.backgroundImage, (0,0))

        if inputs['escape'] == True:
            nextState = Pause(self.main)
            nextState.newState()

        if self.exitButton.draw(screen, inputs) == 1:
            self.leaveState()

         

    #loads assets required for minigame
    def loadImages(self) -> None:
        #loads assets
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/road runner minigame/road runner background.png')
        self.obstacleImage = pygame.image.load(os.getcwd() + '/assets/road runner minigame/obstacle.png')

        #loads character sprite sheets
        self.roadRunnerSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/road runner.png')

        #loads character sprites
        roadRunnerSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/road runner meta.json'), self.roadRunnerSpriteSheet)
        self.roadRunnerSprites = roadRunnerSpritesObject.getSprites()