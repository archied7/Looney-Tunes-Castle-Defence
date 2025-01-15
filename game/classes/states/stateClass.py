import pygame

class State():
    def __init__(self, main: object) -> None:
        self.main = main
        self.loadImages()

    #abstract update function
    def update(self, dt: float, inputs: dict) -> None:
        pass

    #abstract render function
    def render(self, screen: pygame.Surface, inputs: dict) -> None:
        pass

    #abstract function to load images for the state
    def loadImages(self) -> None:
        pass

    def newState(self) -> None:
        self.main.stateStack.append(self)

    def leaveState(self) -> None:
        self.main.stateStack.pop()

