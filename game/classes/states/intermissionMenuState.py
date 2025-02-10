from classes.states.stateClass import State
from classes.buttonClass import Button
from classes.states.pauseState import Pause
import os
import pygame

class IntermissionMenu(State):
    def __init__(self, main: object, castleSlot: int) -> None:
        #intialise parent class
        State.__init__(self, main)

        self.castleSlot = castleSlot

        if self.castleSlot == 1:
            self.x = 575
            self.y = 390

        elif self.castleSlot == 2:
            self.x = 220
            self.y = 400

        elif self.castleSlot == 3:
            self.x = 110
            self.y = 300
        
        elif self.castleSlot == 4:
            self.x = 200
            self.y = 200

        
        self.loadImages()

        #create semi transparent surface
        self.surface = pygame.Surface((1440,900), pygame.SRCALPHA)
        self.surface.fill((0,0,0,100))

        self.grayed = False

        self.owned = [0,0,0,0]
        self.current = []

        #create current heroes list
        for i in self.main.game.currentHeroes:
            self.current.append(self.main.game.currentHeroes[i])

        #create buttons
        self.bugsButton = Button(self.x, self.y+16, self.bugsImage, 1.5, self.bugsHover)
        self.daffyButton = Button(self.x, self.y+75, self.daffyImage, 1.5, self.daffyHover)
        self.tazButton = Button(self.x, self.y+133, self.tazImage, 1.5, self.tazHover)
        self.yosemiteSamButton = Button(self.x, self.y+193, self.yosemiteSamImage, 1.5, self.yosemiteSamHover)

        #set owned heroes list
        if self.main.game.bugsBunny in self.main.game.ownedHeroes:
            self.owned[0] = 1
        if self.main.game.daffyDuck in self.main.game.ownedHeroes:
            self.owned[1] = 1
        if self.main.game.taz in self.main.game.ownedHeroes:
            self.owned[2] = 1
        if self.main.game.yosemiteSam in self.main.game.ownedHeroes:
            self.owned[3] = 1

    def update(self, dt: float, inputs: dict) -> None:
        pygame.display.update()

        #handles leaving state
        if inputs['escape'] == True:
            self.leaveState()

    def render(self, screen, inputs) -> None:
        if self.grayed is not True:
            screen.blit(self.surface, (0,0))
            self.grayed = True

        screen.blit(self.backgroundImage, (self.x, self.y))

        if self.bugsButton.draw(screen, inputs):
            if self.main.game.bugsBunny not in self.current:
                self.main.game.changeHero(self.main.game.bugsBunny, 'add', self.castleSlot)
                self.leaveState()
            else:
                if self.main.game.currentHeroes[self.castleSlot] == self.main.game.bugsBunny:
                    self.main.game.levelHero(self.main.game.bugsBunny)
                else:
                    self.main.game.changeHero(self.main.game.bugsBunny, 'replace', self.castleSlot)
                    self.leaveState()
                    

        if self.daffyButton.draw(screen, inputs):
            if self.owned[1]:
                if self.main.game.daffyDuck not in self.current:
                    self.main.game.currentHeroes[self.castleSlot] = self.main.game.daffyDuck
                    self.leaveState()
                else:
                    if self.main.game.currentHeroes[self.castleSlot] == self.main.game.daffyDuck:
                        self.main.game.levelHero(self.main.game.daffyDuck)
                    else:
                        self.main.game.changeHero(self.main.game.daffyDuck, 'replace', self.castleSlot)
                        self.leaveState()
            else:
                self.main.game.purchaseHero(self.main.game.daffyDuck, self.castleSlot)
                self.leaveState()

        if self.tazButton.draw(screen, inputs):
            if self.owned[2]:
                if self.main.game.taz not in self.current:
                    self.main.game.currentHeroes[self.castleSlot] = self.main.game.taz
                    self.leaveState()
                else:
                    if self.main.game.currentHeroes[self.castleSlot] == self.main.game.taz:
                        self.main.game.levelHero(self.main.game.taz)
                    else:
                        self.main.game.changeHero(self.main.game.taz, 'replace', self.castleSlot)
                        self.leaveState()
            else:
                self.main.game.purchaseHero(self.main.game.taz, self.castleSlot)
                self.leaveState()

        if self.yosemiteSamButton.draw(screen, inputs):
            if self.owned[3]:
                if self.main.game.yosemiteSam not in self.current:
                    self.main.game.currentHeroes[self.castleSlot] = self.main.game.yosemiteSam
                    self.leaveState()
                else:
                    if self.main.game.currentHeroes[self.castleSlot] == self.main.game.yosemiteSam:
                        self.main.game.levelHero(self.main.game.yosemiteSam)
                    else:
                        self.main.game.changeHero(self.main.game.yosemiteSam, 'replace', self.castleSlot)
                        self.leaveState()
            else:
                self.main.game.purchaseHero(self.main.game.yosemiteSam, self.castleSlot)
                self.leaveState()
        
        self.main.drawText('OWNED', self.x+14, self.y+28, 11, 'green')
        self.main.drawText('LEVEL: ' + str(self.main.game.bugsBunny.level), self.x+14, self.y+38, 11, 'black')
        self.main.drawText('UPGRADE: ', self.x+14, self.y+48, 11)
        self.main.drawText(str(self.main.game.bugsBunny.upgradePrice), self.x+14, self.y+58, 11)


        if self.owned[1]:
            self.main.drawText('OWNED', self.x+14, self.y+87, 11, 'green')
            self.main.drawText('LEVEL: ' + str(self.main.game.daffyDuck.level), self.x+14, self.y+97, 11, 'black')
            self.main.drawText('UPGRADE: ', self.x+14, self.y+107, 11)
            self.main.drawText(str(self.main.game.daffyDuck.upgradePrice), self.x+14, self.y+117, 11)
        else:
            self.main.drawText('COST: 100', self.x+14, self.y+87, 11)

        if self.owned[2]:
            self.main.drawText('OWNED', self.x+14, self.y+145, 11, 'green')
            self.main.drawText('LEVEL: ' + str(self.main.game.taz.level), self.x+14, self.y+155, 11, 'black')
            self.main.drawText('UPGRADE: ', self.x+14, self.y+165, 11)
            self.main.drawText(str(self.main.game.taz.upgradePrice), self.x+14, self.y+175, 11)
        else:
            self.main.drawText('COST: 100', self.x+14, self.y+145, 11)
        
        if self.owned[3]:
            self.main.drawText('OWNED', self.x+14, self.y+217, 11, 'green')
            self.main.drawText('LEVEL: ' + str(self.main.game.yosemiteSam.level), self.x+14, self.y+227, 11, 'black')
            self.main.drawText('UPGRADE:'+str(self.main.game.yosemiteSam.upgradePrice), self.x+14, self.y+237, 11)
        else:
            self.main.drawText('COST: 100', self.x+14, self.y+217, 11)

        

    def loadImages(self):
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/main game/upgrade background.png')
        self.backgroundImage = pygame.transform.scale_by(self.backgroundImage, 1.5)
        self.bugsImage = pygame.image.load(os.getcwd() + '/assets/main game/upgrade button 1.png')
        self.bugsHover = pygame.image.load(os.getcwd() + '/assets/main game/upgrade button 1 hover.png')
        self.daffyImage = pygame.image.load(os.getcwd() + '/assets/main game/upgrade button 2.png')
        self.daffyHover = pygame.image.load(os.getcwd() + '/assets/main game/upgrade button 2 hover.png')
        self.tazImage = pygame.image.load(os.getcwd() + '/assets/main game/upgrade button 3.png')
        self.tazHover = pygame.image.load(os.getcwd() + '/assets/main game/upgrade button 3 hover.png')
        self.yosemiteSamImage = pygame.image.load(os.getcwd() + '/assets/main game/upgrade button 4.png')
        self.yosemiteSamHover = pygame.image.load(os.getcwd() + '/assets/main game/upgrade button 4 hover.png')

        

        
class TowerIntermissionMenu(State):
    def __init__(self, main):
        State.__init__(self, main)
        self.loadImages()
        self.x, self.y = 575, 575

        self.surface = pygame.Surface((1440,900), pygame.SRCALPHA)
        self.surface.fill((0,0,0,100))

        self.grayed = False

        self.owned = self.main.game.ownedTowers
        self.current = self.main.game.currentTower

        self.healthButton = Button(self.x, self.y+17, self.healthTowerImage, 1.5, self.healthTowerImageHover)
        self.goldButton = Button(self.x, self.y+75, self.goldTowerImage, 1.5, self.goldTowerImageHover)

    def update(self, dt, inputs):
        pygame.display.update()

        if inputs['escape']:
            self.leaveState()

    def render(self, screen, inputs):
        if self.grayed is not True:
            screen.blit(self.surface, (0,0))
            self.grayed = True

        screen.blit(self.backgroundImage, (self.x, self.y))

        if self.healthButton.draw(screen, inputs):
            if self.current == self.main.game.healthTower:
                self.leaveState()
            else:
                if self.main.game.healthTower in self.owned:
                    self.main.game.changeTower(self.main.game.healthTower, 'replace')
                    self.leaveState()
                else:
                    if self.current:
                        self.current.remove(self.main.game)
                    
                    self.main.game.purchaseTower(self.main.game.healthTower)
                    self.leaveState()

        
        if self.goldButton.draw(screen, inputs):
            if self.current == self.main.game.goldTower:
                self.leaveState()
            else:
                if self.main.game.goldTower in self.owned:
                    self.main.game.changeTower(self.main.game.goldTower, 'replace')
                    self.leaveState()
                else:
                    if self.current:
                        self.current.remove(self.main.game)
                    self.main.game.purchaseTower(self.main.game.goldTower)
                    self.leaveState()

        if self.main.game.healthTower in self.owned:
            self.main.drawText('OWNED', self.x+14, self.y+28, 11, 'green')
        else:
            self.main.drawText('COST: ' + str(self.main.game.healthTower.cost), self.x+14, self.y+28, 11)

        if self.main.game.goldTower in self.owned:
            self.main.drawText('OWNED', self.x+14, self.y+87, 11, 'green')
        else:
            self.main.drawText('COST: ' + str(self.main.game.goldTower.cost), self.x+14, self.y+87, 11)


    def loadImages(self):
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/main game/tower upgrade background.png')
        self.backgroundImage = pygame.transform.scale_by(self.backgroundImage, 1.5)
        self.healthTowerImage = pygame.image.load(os.getcwd() + '/assets/main game/health upgrade button.png')
        self.healthTowerImageHover = pygame.image.load(os.getcwd() + '/assets/main game/health upgrade button hover.png')
        self.goldTowerImage = pygame.image.load(os.getcwd() + '/assets/main game/gold upgrade button.png')
        self.goldTowerImageHover = pygame.image.load(os.getcwd() + '/assets/main game/gold upgrade button hover.png')
