import pygame
import time
import os
from classes import gameClass, buttonClass, stateClass

class Main():
    #initialise Main class
    def __init__(self) -> None:
        #set game window
        self.WIDTH = 1440
        self.HEIGHT = 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.canvas = pygame.Surface((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption('Looney Tunes Castle Defence')
        icon = pygame.image.load(os.path.dirname(os.path.dirname(__file__)) + "/assets/misc/icon.png")
        pygame.display.set_icon(icon)

        #set variables
        self.running = True
        self.dt = 0
        self.previousTime = 0
        self.FPS = 30
        self.stateStack = []

    #loads images
    def loadImages(self) -> None:
        self.assetsFolder = os.path.join("assets")
        self.charactersFolder = os.path.join(self.assetsFolder, "characters")
        self.mainGameFolder = os.path.join(self.assetsFolder, "main game")
        self.mainMenuFolder = os.path.dirname(os.path.dirname(__file__)) + "/assets/main menu"
        self.roadRunnerMinigame = os.path.join(self.assetsFolder, "road runner minigame")
        self.tweetyPieMinigame = os.path.join(self.assetsFolder, "tweety pie minigame")
        self.miscFolder = os.path.join(self.assetsFolder, "misc")
    
    #game loop
    def gameLoop(self) -> None:
        self.loadImages()
        while self.running:
            self.get_dt()
            self.getEvents()
            self.update()
            self.render()
            print(self.mainMenuFolder)

    #gets pygame events and responds to them
    def getEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
    def update(self) -> None:
        pass

    #renders game screen
    def render(self) -> None:
        self.screen.blit(self.canvas, (0,0))

    #sets delta time value
    def get_dt(self) -> None:
        timeNow = time.time()
        self.dt = timeNow - self.previousTime
        self.previousTime = timeNow
    


if __name__ == "__main__":
    game = Main()
    while game.running:
        game.gameLoop()