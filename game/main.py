import pygame
import time
import os
from classes.states import mainMenuState

class Main():
    #initialise Main class
    def __init__(self) -> None:
        pygame.init()
        #set game window
        self.WIDTH = 1440
        self.HEIGHT = 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption('Looney Tunes Castle Defence')
        icon = pygame.image.load(os.path.dirname(os.path.dirname(__file__)) + "/assets/misc/icon.png")
        pygame.display.set_icon(icon)

        #set variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.previousTime = 0
        self.FPS = 30
        self.stateStack = []
        self.inputs = {}

    #initialises states
    def loadStates(self) -> None:
        self.mainMenu = mainMenuState.MainMenu(self)
        self.stateStack.append(self.mainMenu )

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
    #calls update function from the current state
    def update(self) -> None:
        self.stateStack[-1].update(self.dt)

    #calls the render function from the current state
    def render(self) -> None:
        self.stateStack[-1].render(self.screen)
        

    #sets delta time value
    def get_dt(self) -> None:
        timeNow = time.time()
        self.dt = timeNow - self.previousTime
        self.previousTime = timeNow

if __name__ == "__main__":
    game = Main()
    while game.running:
        game.gameLoop()