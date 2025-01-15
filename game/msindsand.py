import pygame
import time
import os
from classes.states import mainMenuState
from classes.gameClass import Game

#intiialises pygame
pygame.init()

class Main():
    #initialise Main class
    def __init__(self) -> None:
        self.game = Game()

        #set game window
        self.WIDTH = 1440
        self.HEIGHT = 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption('Looney Tunes Castle Defence')
        icon = pygame.image.load(os.getcwd() + "/assets/misc/icon.png")
        pygame.display.set_icon(icon)

        #set variables
        self.clicked = False
        self.inputs = {"escape" : False, "click": False}
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.previousTime = 0
        self.FPS = 30
        self.stateStack = []

    #initialises states
    def loadStates(self) -> None:
        self.mainMenu = mainMenuState.MainMenu(self)
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

        if self.clicked == True:
            self.inputs['click'] = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            #gets key presses
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.inputs['click'] = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.inputs['escape'] = True


            #turns key presses off once they are not clicked
            if pygame.mouse.get_pressed()[0] == 0:
                self.inputs['click'] = False
                self.clicked = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.inputs['escape'] = False

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

if __name__ == "__main__":
    game = Main()
    while game.running:
        game.gameLoop()