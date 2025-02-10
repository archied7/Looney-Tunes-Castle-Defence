from classes.states.stateClass import State
from classes.spriteLoader import SpriteLoader
from classes.states.pauseState import Pause
from classes.buttonClass import Button
import pygame
import random
import math
import os

class RoadRunner(State):
    def __init__(self, main: object) -> None:
        #initialise parent class
        State.__init__(self, main)

        #create exit button
        self.exitButton = Button(538, 660, self.main.exitImage, 2.5, self.main.exitHoverImage)

        #initialise variables used for timers
        self.startTicks = pygame.time.get_ticks()
        self.currentTickDifference = 0

        #set variables
        self.multiplier = 1
        self.scrollSpeed = 20
        self.barrelFreq = 175 
        self.lastBarrel = pygame.time.get_ticks() - self.barrelFreq
        self.groundScroll = -900
        self.alive = True
        self.result = False
        self.goldAdded = False

        #set the timer depending on the current round, maxed out at 45 seconds
        if self.main.game.round <= 36:
            self.timer = 14 + self.main.game.round
        else:
            self.timer = 45

        #create runner object and sprite group for objects
        self.runner = Runner(720, 775)
        self.barrelGroup = pygame.sprite.Group()

    def update(self, dt: float, inputs: dict) -> None:
        pygame.display.update()

        if self.alive:
            self.runner.update(dt, inputs, self.main.FPS, self.multiplier)

            if self.runner.isMoving:
                timeNow = pygame.time.get_ticks()
                self.barrelGroup.update(dt, self.main.FPS, self.scrollSpeed, self.multiplier)

                #handles acceleration
                if inputs['up']:
                    if self.multiplier < 2.25:
                        self.multiplier *= 1.05
                    else:
                        self.multiplier = 2.25
                    
                #handles deceleration
                else:
                    if self.multiplier > 1:
                        self.multiplier *= 0.9
                    else:
                        self.multiplier = 1

                #checks for rect collisions
                collisionList = pygame.sprite.spritecollide(self.runner, self.barrelGroup, False)
                if collisionList != []:
                    #checks for pixel perfect collisions
                    self.runner.getMask()
                    
                    collisionGroup = pygame.sprite.Group()
                    for i in collisionList:
                        i.getMask()
                        collisionGroup.add(i)

                    #if a collision has occured
                    if pygame.sprite.spritecollide(self.runner, collisionGroup, False, pygame.sprite.collide_mask):
                        self.alive = False
                    

                #handles pausing ticks
                if self.main.game.paused == True:
                    self.startTicks = pygame.time.get_ticks() - self.currentTickDifference
                    self.main.game.changePause()
                    
                #timer
                seconds = (pygame.time.get_ticks() - self.startTicks)/1000 * self.multiplier
                if math.floor(seconds) >= 1:
                    self.startTicks = pygame.time.get_ticks()
                    if self.timer > 1:
                        self.timer -= 1
                    else:
                        self.alive = False
                        self.result = True

                #generates obstacles
                if timeNow - self.lastBarrel > self.barrelFreq:
                    x1 = random.randint(0, 1344)
                    barrel1 = Obstacle(x1, -100, self.obstacleImage)
                    self.barrelGroup.add(barrel1)
                    self.lastBarrel = pygame.time.get_ticks()


                #scrolls the ground
                self.groundScroll += self.scrollSpeed * self.main.FPS * dt * self.multiplier
                if self.groundScroll > 0:
                    self.groundScroll = -900 

        else:
            #if the user completed the minigame, add relevant gold
            if self.result:
                if self.goldAdded == False:
                    self.main.minigameValue = self.main.game.changeGold(self.main.minigameValue, False)
                    self.goldAdded = True

            

    def render(self, screen: pygame.Surface, inputs: dict) -> None:
        #handles pausing
        if inputs['escape'] == True:
            nextState = Pause(self.main)
            self.currentTickDifference = pygame.time.get_ticks() - self.startTicks
            nextState.newState()

        #draws every object onto the screen
        screen.fill((0,0,0))
        screen.blit(self.backgroundImage, (0,self.groundScroll))

        self.runner.render(screen)
        self.barrelGroup.draw(screen)

        #draws the timer
        self.main.drawText(str(self.timer), 10, 10, 60)
                
        #draws tutorial image
        if self.runner.isMoving == False:
            screen.blit(self.tutorialImage, (self.main.WIDTH/2 - self.tutorialImage.get_width()/2,
                                              self.main.HEIGHT/2 - self.tutorialImage.get_height()/2))

        #draws exit button when the minigame is complete
        if self.alive == False:
            if self.exitButton.draw(screen, inputs) == 1:
                self.leaveState()

    #loads assets required for minigame
    def loadImages(self) -> None:
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/road runner minigame/road runner background.png')
        self.obstacleImage = pygame.image.load(os.getcwd() + '/assets/road runner minigame/obstacle.png')
        self.tutorialImage = pygame.image.load(os.getcwd() + '/assets/road runner minigame/road runner tutorial.png')
        self.tutorialImage = pygame.transform.scale_by(self.tutorialImage, 2.5)

class Runner():
    def __init__(self, x: int, y: int) -> None:
        #loads sprites
        self.loadSprites()

        #sets variables
        self.currentFrameNum = 1
        self.isMoving = False
        self.x, self.y = x, y
        self.lastUpdate = 0

        #creates current rect
        self.image = self.roadRunnerFrames[0]

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


    def update(self, dt: float, inputs: dict, fps: int, multiplier: float):
        if self.isMoving:
            #animates the road runner
            self.animate(dt, multiplier)

            #handles movement with framrate independence
            if inputs['left']:
                if self.x > 55:
                    self.x -= 15 * multiplier * dt * fps
            if inputs['right']:
                if self.x < 1385:
                    self.x += 15 * multiplier * dt * fps

            self.rect.center = (self.x, self.y)

        #handles starting the game
        else:
            if inputs['up']:
                self.isMoving = True

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def animate(self, dt: float, multiplier: float) -> None:
        #handles animation
        self.lastUpdate += dt * multiplier

        if self.lastUpdate > 0.1:
            self.lastUpdate = 0
            self.currentFrameNum += 1

            #animaties between frame 0 and 2
            self.image = self.roadRunnerFrames[(self.currentFrameNum % 3)]

            #creates new rect
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

    def getMask(self) -> None:
        #creates mask for current location of runner
        self.mask = pygame.mask.from_surface(self.image)

    def loadSprites(self) -> None:
        roadRunnerSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/road runner.png')
        roadRunnerSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/road runner meta.json'), roadRunnerSpriteSheet, True)
        self.roadRunnerFrames = roadRunnerSpritesObject.getSpritesList()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface) -> None:
        #initialise sprite
        pygame.sprite.Sprite.__init__(self)

        #set initial rect
        self.image = pygame.transform.scale_by(image, 3)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def update(self, dt: float, fps: int, scrollSpeed: int, multiplier: float) -> None:
        #moves the obstacle down the screen
        self.rect.y += scrollSpeed * dt * fps * multiplier

        #kills the obstacle when it leaves the screen
        if self.rect.y > 900:
            self.kill()

    def getMask(self) -> None:
        #creates a mask for the current location of the obstacle
        self.mask = pygame.mask.from_surface(self.image)
