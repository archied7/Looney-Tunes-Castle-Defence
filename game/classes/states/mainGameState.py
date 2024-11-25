from classes.states.stateClass import State
from classes.spriteLoader import SpriteLoader
from classes.states.minigameSelectState import MinigameSelect
from classes.states.pauseState import Pause
from classes.buttonClass import Button
import pygame
import os

class MainGame(State):
    def __init__(self, main) -> None:
        State.__init__(self, main)

    def update(self, dt, inputs) -> None:
        pygame.display.update()
        if pygame.mouse.get_pressed()[0] == 1:
            nextState = MinigameSelect(self.main)
            nextState.newState()

    def render(self, screen, inputs) -> None:
        screen.fill((0,0,0))
        screen.blit(self.backgroundImage, (0,0))
        
        self.main.drawText('GOLD: ' + str(self.main.game.getGold()), 10, 10, screen, 30)

        if inputs['escape'] == True:
            nextState = Pause(self.main)
            nextState.newState()


    #loads images required for the main game
    def loadImages(self) -> None:
        #loads assets
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/main game/main background.png')
        self.castleImage = pygame.image.load(os.getcwd() + '/assets/main game/castle.png')
        self.goldTowerImage = pygame.image.load(os.getcwd() + '/assets/main game/gold tower.png')
        self.healthTowerImage = pygame.image.load(os.getcwd() + '/assets/main game/health tower.png')
       
        #loads character sprite sheets used in main game
        self.bugsBunnySpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/bugs bunny.png')
        self.daffyDuckSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/daffy duck.png')
        self.elmerFuddSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/elmer fudd.png')
        self.marvinMartianSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/marvin martian.png')
        self.sylvesterSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/sylvester pussycat.png')
        self.tazSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/taz.png')
        self.yosemiteSamSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/yosemite sam.png')

        #loads dicts containing individual sprites
        bugsSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/bugs bunny meta.json'), self.bugsBunnySpriteSheet)
        self.bugsSprites = bugsSpritesObject.getSprites()

        daffyDuckSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/daffy duck meta.json'), self.daffyDuckSpriteSheet)
        self.daffySprites = daffyDuckSpritesObject.getSprites()

        sylvesterSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/sylvester pussycat meta.json'), self.sylvesterSpriteSheet)
        self.sylvesterSprites = sylvesterSpritesObject.getSprites()

        

