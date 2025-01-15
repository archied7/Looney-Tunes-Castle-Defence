from classes.states.stateClass import State
from classes.states.mainGameState import MainGame
from classes.buttonClass import Button
import pygame
import os
class MainMenu(State):
    def __init__(self, main: object) -> None:
        #initialises the parent class
        State.__init__(self, main)

        #creates the start button
        self.mainMenuButton = Button(600,750, self.buttonImage, 0.8, self.buttonPressedImage, 1)

        self.pressed = False

        #loads save file
        self.main.saveLoadManager.load()
    
    #updates the screen and checks for button press
    def update(self, dt: float, inputs: dict) -> None:
        pygame.display.update()
        if self.pressed:
            nextState = MainGame(self.main)
            nextState.newState()

    #draws the main menu and button onto the screen
    def render(self, screen: pygame.Surface, inputs: dict) -> None:
        screen.fill((0,0,0))
        screen.blit(self.mainMenuImage, (0,0))
        
        #checks if the start button has been pressed
        if self.mainMenuButton.draw(screen, inputs) == 1:
            self.pressed = True

    #loads the images required for the main menu
    def loadImages(self) -> None:
        self.menuImage = pygame.image.load(os.getcwd() + '/assets/main menu/main menu.png')
        self.mainMenuImage = pygame.transform.scale(self.menuImage, (self.main.WIDTH, self.main.HEIGHT))
        self.buttonImage = pygame.image.load(os.getcwd() + '/assets/main menu/main menu start.png')
        self.buttonPressedImage = pygame.image.load(os.getcwd() + '/assets/main menu/main menu start pressed.png')
