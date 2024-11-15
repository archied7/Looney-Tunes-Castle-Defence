from classes.states.stateClass import State
from classes.spriteLoader import SpriteLoader
import pygame
import os

class MainGame(State):
    def __init__(self, main) -> None:
        self.spriteScale = 10
        State.__init__(self, main)

    def update(self, dt) -> None:
        pygame.display.update()

    def render(self, screen) -> None:
        screen.fill((0,0,0))
        screen.blit(self.backgroundImage, (0,0))
        screen.blit(self.bugsSprites['stand'], (50,50))
        screen.blit(self.bugsSprites['ability1'], (200,50))

    #loads images required for the main game
    def loadImages(self) -> None:
        #loads assets
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/main game/main background.png')
        self.castleImage = pygame.image.load(os.getcwd() + '/assets/main game/castle.png')
        self.goldTowerImage = pygame.image.load(os.getcwd() + '/assets/main game/gold tower.png')
        self.healthTowerImage = pygame.image.load(os.getcwd() + '/assets/main game/health tower.png')

        #loads character sprite sheets used in main game
        self.bugsBunnySprites = pygame.image.load(os.getcwd() + '/assets/characters/bugs bunny.png')
        self.daffyDuckSprites = pygame.image.load(os.getcwd() + '/assets/characters/daffy duck.png')
        self.elmerFuddSprites = pygame.image.load(os.getcwd() + '/assets/characters/elmer fudd.png')
        self.marvinMartianSprites = pygame.image.load(os.getcwd() + '/assets/characters/marvin martian.png')
        self.sylvesterSprites = pygame.image.load(os.getcwd() + '/assets/characters/sylvester pussycat.png')
        self.tazSprites = pygame.image.load(os.getcwd() + '/assets/characters/taz.png')
        self.yosemiteSamSprites = pygame.image.load(os.getcwd() + '/assets/characters/yosemite sam.png')

        self.bugsSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/bugs bunny meta.json'), self.bugsBunnySprites)
        self.bugsSprites = self.bugsSpritesObject.getSprites()

