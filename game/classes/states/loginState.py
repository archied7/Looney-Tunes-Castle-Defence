import sqlite3
import os
import pygame
from classes.states.mainMenuState import MainMenu
from classes.buttonClass import Button
from classes.states.stateClass import State
from classes.states.pauseState import Pause


class Login(State):
    def __init__(self, main: object, dbFile: str) -> None:
        """
        currentInput = 0 if typing username
                     = 1 if typing password 
        """
        State.__init__(self, main)
        self.db = dbFile
        self.passwordSuccess = True
        self.createUserSuccess = True

        self.loginButton = Button(600, 650, self.loginButtonImage, 1.5, self.loginButtonHoverImage)
        self.createUserButton = Button(600, 750, self.createUserButtonImage, 1.5, self.createUserButtonImageHover)
        self.eyeButton = Button(1060, 555, self.eyeClosedImage, 2)

        self.usernameButton = Button(300, 400, self.inputButtonImage, 1)
        self.passwordButton = Button(300, 550, self.inputButtonImage, 1)

        self.indicator = 10
        self.currentInput = 0
        self.eyeState = 'closed'

        self.usernameText = ''
        self.passwordText = ''

    def update(self, dt: float, inputs: dict) -> None:
        pygame.display.update()

        #handles user input
        if inputs['input'] != None:
            if self.currentInput == 0:
                self.usernameText += inputs['input']
            else:
                self.passwordText += inputs['input']
        if inputs['backspace']:
            if self.currentInput == 0:
                self.usernameText = self.usernameText[:-1]
            else:
                self.passwordText = self.passwordText[:-1]

        #handles flashing cursor
        self.indicator -= 1 * dt * self.main.FPS
        if self.indicator <= -10:
            self.indicator = 10

        #handles pausing
        if inputs['escape']:
            nextState = Pause(self.main)
            nextState.newState()

    def render(self, screen: pygame.Surface, inputs: dict) -> None:
        screen.fill((40,40,40))

        #draws buttons
        if self.usernameButton.draw(screen, inputs):
            self.currentInput = 0

        if self.passwordButton.draw(screen, inputs):
            self.currentInput = 1

        self.main.drawText('USERNAME', 300, 350, 30, 'green')
        self.main.drawText('PASSWORD', 300, 500, 30, 'green')

        #handles hiding password
        if self.eyeState == 'closed':
            text = '*' * len(self.passwordText)
        else:
            text = self.passwordText

        #handles error messages
        if self.passwordSuccess == False:
            self.main.drawText('INCORRECT USERNAME OR PASSWORD', 510, 600, 20, 'red')
        elif self.createUserSuccess == False:
            self.main.drawText('USERNAME ALREADY EXISTS OR EMPTY FIELD', 455, 600, 20, 'red')
        
        #handles indicator
        if self.currentInput == 0:
            if self.indicator >= 0:
                self.main.drawText(self.usernameText + '|', 310, 410, 20, 'black')
            else:
                self.main.drawText(self.usernameText + '', 310, 410, 20, 'black')
            self.main.drawText(text, 310, 560, 20, 'black')
        else:
            self.main.drawText(self.usernameText, 310, 410, 20, 'black')
            if self.indicator >= 0:
                self.main.drawText(text + '|', 310, 560, 20, 'black')
            else:
                self.main.drawText(text + '', 310, 560, 20, 'black')


        #handles eye button
        if self.eyeButton.draw(screen, inputs):
            if self.eyeState == 'closed':
                self.eyeButton.changeImage(self.eyeOpenImage, 2)
                self.eyeState = 'open'
            else:
                self.eyeButton.changeImage(self.eyeClosedImage, 2)
                self.eyeState = 'closed'


        #handles login
        if self.loginButton.draw(screen, inputs):
            hashedPass = self.hash(self.passwordText)
            with sqlite3.connect(self.db) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT hashedpassword FROM UserData WHERE username = ? ''', (str(self.usernameText),))
                dbPass = cursor.fetchone()
                if dbPass is not None:
                    dbPass = dbPass[0]
                    if hashedPass == dbPass:
                        cursor.execute('''SELECT userID FROM UserData WHERE username = ? ''', (str(self.usernameText),))
                        self.main.saveLoadManager.userID = str(cursor.fetchone()[0])

                        nextState = MainMenu(self.main)
                        nextState.newState()
            self.passwordSuccess = False
            self.createUserSuccess = True

        #handles creating new user
        if self.createUserButton.draw(screen, inputs):
            newID = self.main.saveLoadManager.newSave()
            if self.passwordText != '' and self.usernameText != '':
                hashedPass = self.hash(self.passwordText)
                with sqlite3.connect(self.db) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''SELECT 0 FROM UserData WHERE username = ? ''', (str(self.usernameText),))
                    usernameValid = cursor.fetchone()
                    if usernameValid == None:
                        cursor.execute('''
                                    INSERT INTO UserData (userID, username, hashedpassword)
                                    VALUES (?,?,?)''', (newID, self.usernameText, hashedPass))
                        
                        conn.commit()
                        nextState = MainMenu(self.main)
                        nextState.newState()
            self.createUserSuccess = False
            self.passwordSuccess = True
                        


    def hash(self, data: str, index: int=0, hashVal=0) -> str:
        if index == len(data):
            return f'{hashVal:0256x}'
        
        hashVal = (hashVal * 31 + ord(data[index])) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        #recursively calls itself until hash is complete
        return self.hash(data, index + 1, hashVal)
    
    def loadImages(self) -> None:
        self.loginButtonImage = pygame.image.load(os.getcwd() + '/assets/misc/login button.png')
        self.loginButtonHoverImage = pygame.image.load(os.getcwd() + '/assets/misc/login button hover.png')
        self.inputButtonImage = pygame.image.load(os.getcwd() + '/assets/misc/input button.png')
        self.createUserButtonImage = pygame.image.load(os.getcwd() + '/assets/misc/create user button.png')
        self.createUserButtonImageHover = pygame.image.load(os.getcwd() + '/assets/misc/create user button hover.png')
        self.eyeClosedImage = pygame.image.load(os.getcwd() + '/assets/misc/eye closed.png')
        self.eyeOpenImage = pygame.image.load(os.getcwd() + '/assets/misc/eye open.png')