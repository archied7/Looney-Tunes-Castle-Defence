class State():
    def __init__(self, main) -> None:
        self.main = main
        self.previousState = None
        self.loadImages()

    #abstract update function
    def update(self) -> None:
        pass

    #abstract render function
    def render(self) -> None:
        pass

    #abstract function to load images for the state
    def loadImages(self) -> None:
        pass

    def newState(self) -> None:
        if len(self.main.stateStack) > 1:
            self.previousState = self.main.stateStack[-1]
        self.main.stateStack.append(self)

    def leaveState(self) -> None:
        self.main.stateStack.pop()