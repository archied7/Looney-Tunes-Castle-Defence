from stateClass import State
import pygame

class MainMenu(State):
    def __init__(self, main):
        super.__init__(self, main)
        self.loadImages()
    
    def update(self) -> None:
        pass

    def render(self, screen) -> None:
        screen.fill((0,0,0))
        mainMenuImage = pygame.transform.scale(menuImage, (w, h))
        screen.blit(mainMenuImage, (0,0))

        
    def loadImages(self) -> None:
        self.mainMenuImage = pygame.image.load(main.mainMenuFolder + "main menu.png")

