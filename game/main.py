import pygame
import time
import os
from classes.states.loginState import Login
from classes.gameClass import Game
from classes.saveLoadManagerClass import SaveLoadManager

pygame.init()
font11 = pygame.font.Font(os.getcwd() + '/assets/misc/font.ttf', 11)
font15 = pygame.font.Font(os.getcwd() + '/assets/misc/font.ttf', 15)
font20 = pygame.font.Font(os.getcwd() + '/assets/misc/font.ttf', 20)
font30 = pygame.font.Font(os.getcwd() + '/assets/misc/font.ttf', 30)
font60 = pygame.font.Font(os.getcwd() + '/assets/misc/font.ttf', 60)

class Main():
    #initialise Main class
    def __init__(self) -> None:
        self.game = Game()

        userID = 'guest'
        self.saveLoadManager = SaveLoadManager((os.getcwd() + '/saveData/data.json'), self, userID)

        
        #set game window
        self.WIDTH = 1440
        self.HEIGHT = 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption('Looney Tunes Castle Defence')
        icon = pygame.image.load(os.getcwd() + "/assets/misc/icon.png")
        pygame.display.set_icon(icon)

        #loads global images
        self._exitImage = pygame.image.load(os.getcwd() + '/assets/misc/exit.png')
        self._exitHoverImage = pygame.image.load(os.getcwd() + '/assets/misc/exit hover.png')

        #set variables
        self.inputs = {"escape": False, "click": False, "left": False, "right": False, "up": False, "backspace": False, "input": None}
        self.inputsPressed = {"escape": False, "click": False, "backspace": False, "input":False}
        self.clock = pygame.time.Clock()
        self._running = True
        self.dt = 0
        self.previousTime = 0
        self._FPS = 30
        self.stateStack = []
        self._minigameValue = int(self.game.gold * 0.10) if int(self.game.gold*0.1) >=1 else 1

        self._survivedRound = True

    #initialises states
    def loadStates(self) -> None:
        self.mainMenu = Login(self, os.getcwd() + '/saveData/users.db')
        self.mainMenu.newState()

    #game loop
    def gameLoop(self) -> None:
        self.loadStates()

        while self.running:
            self.clock.tick(self.FPS)
            self.get_dt()
            self.getEvents()
            self.update()
            self.render()

    #gets pygame events and responds to them
    def getEvents(self) -> None:
        if self.inputsPressed['click']:
            self.inputs['click'] = False
        if self.inputsPressed['escape']:
            self.inputs['escape'] = False
        if self.inputsPressed['backspace']:
            self.inputs['backspace'] = False
        if self.inputsPressed['input']:
            self.inputs['input'] = None

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            #gets key presses
            if pygame.mouse.get_pressed()[0] == 1 and self.inputsPressed['click'] == False:
                self.inputsPressed['click'] = True
                self.inputs['click'] = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.inputsPressed['escape'] == False:
                    self.inputsPressed['escape'] = True
                    self.inputs['escape'] = True
                if event.key == pygame.K_LEFT:
                    self.inputs['left'] = True
                if event.key == pygame.K_BACKSPACE and self.inputsPressed['backspace'] == False:
                    self.inputsPressed['backspace'] = True
                    self.inputs['backspace'] = True
                if event.key == pygame.K_RIGHT:
                    self.inputs['right'] = True
                if event.key == pygame.K_UP:
                    self.inputs['up'] = True
                else:
                    if self.inputsPressed['input'] == False:
                        self.inputsPressed['input'] = True
                        self.inputs['input'] = event.unicode


            #turns key presses off once they are not clicked
            if pygame.mouse.get_pressed()[0] == 0:
                self.inputs['click'] = False
                self.inputsPressed['click'] = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.inputs['escape'] = False
                    self.inputsPressed['escape'] = False
                if event.key == pygame.K_LEFT:
                    self.inputs['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.inputs['right'] = False
                if event.key == pygame.K_UP:
                    self.inputs['up'] = False
                if event.key == pygame.K_BACKSPACE:
                    self.inputs['backspace'] = False
                    self.inputsPressed['backspace'] = False
                else:
                    self.inputs['input'] = None
                    self.inputsPressed['input'] = False
            

    #calls update function from the current state
    def update(self) -> None:
        self.stateStack[-1].update(self.dt, self.inputs)

    #calls the render function from the current state
    def render(self) -> None:
        self.stateStack[-1].render(self.screen, self.inputs)

    #sets delta time value
    def get_dt(self) -> None:
        timeNow = time.time()
        self.dt = timeNow - self.previousTime
        self.previousTime = timeNow

    def drawText(self, text: str, x: int, y: int, size: int, colour: str='gold') -> None:
        if colour == 'gold':
            rgb = (255,215,0)
        elif colour == 'red':
            rgb = (120, 6, 6)
        elif colour == 'black':
            rgb = (0,0,0)
        elif colour == 'green':
            rgb = (10, 138, 54)

        if size == 11:
            image = font11.render(text, True, rgb)
        elif size == 15:
            image = font15.render(text, True, rgb)
        elif size == 20:
            image = font20.render(text, True, rgb)
        elif size == 30:
            image = font30.render(text, True, rgb)
        elif size == 60:
            image = font60.render(text, True, rgb)
            
        self.screen.blit(image, (x,y))


    #getters and setters
    @property
    def FPS(self) -> int:
        return self._FPS
    
    @property
    def exitImage(self) -> pygame.Surface:
        return self._exitImage
    
    @property
    def exitHoverImage(self) -> pygame.Surface:
        return self._exitHoverImage


    @property
    def running(self) -> bool:
        return self._running
    @running.setter
    def running(self, val: bool) -> None:
        self._running = val

    

    @property
    def minigameValue(self) -> int:
        return self._minigameValue
    @minigameValue.setter
    def minigameValue(self, val: int) -> None:
        self._minigameValue = val


    @property
    def survivedRound(self) -> bool:
        return self._survivedRound
    @survivedRound.setter
    def survivedRound(self, val: bool) -> None:
        self._survivedRound = val



if __name__ == "__main__":
    game = Main()
    while game.running:
        game.gameLoop()