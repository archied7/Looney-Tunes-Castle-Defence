from classes.states.stateClass import State
from classes.spriteLoader import SpriteLoader
from classes.states.pauseState import Pause
from classes.buttonClass import Button
import pygame
import math
import os

class RoadRunner(State):
    def __init__(self, main) -> None:
        State.__init__(self, main)
        self.exitButton = Button(538, 660, self.main.exitImage, 2.5, self.main.exitHoverImage)

        self.startTicks = pygame.time.get_ticks()
        self.currentTickDifference = 0

        self.scrollSpeed = 5
        self.groundScroll = 0
        self.timer = 5
        self.alive = True
        self.result = False
        self.goldAdded = False
        self.moving = True

        self.runner = Runner(720, 700)

    def update(self, dt, inputs) -> None:
        pygame.display.update()

        if self.alive:
            if self.moving:
                self.runner.update(dt, inputs, self.main.FPS)

                #timer
                if self.main.game.getPause() == True:
                    self.startTicks = pygame.time.get_ticks() - self.currentTickDifference
                    self.main.game.changePause()
                    
                seconds = (pygame.time.get_ticks() - self.startTicks)/1000
                if math.floor(seconds) >= 1:
                    self.startTicks = pygame.time.get_ticks()
                    if self.timer > 0:
                        self.timer -= 1
                    else:
                        self.alive = False
                        self.result = True

                #generates obstacles
                


                #scrolls the ground
                self.groundScroll -= self.scrollSpeed * self.main.FPS * dt
                if abs(self.groundScroll) > 35:
                    self.groundScroll = 0     

        else:
            if self.result:
                if self.goldAdded == False:
                    self.main.minigameValue = self.main.game.changeGold(self.main.minigameValue, False)
                    self.goldAdded = True

            

    def render(self, screen, inputs) -> None:
        if inputs['escape'] == True:
            nextState = Pause(self.main)
            self.currentTickDifference = pygame.time.get_ticks() - self.startTicks
            nextState.newState()

        if self.alive:
            screen.fill((0,0,0))
            screen.blit(self.backgroundImage, (0,self.groundScroll))

            self.runner.render(screen)

            self.main.drawText(str(self.timer), 10, 10, screen, 60)
                    
        else:
            if self.exitButton.draw(screen, inputs) == 1:
                self.leaveState()

    #loads assets required for minigame
    def loadImages(self) -> None:
        #loads assets
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/road runner minigame/road runner background.png')
        self.obstacleImage = pygame.image.load(os.getcwd() + '/assets/road runner minigame/obstacle.png')

class Runner():
    def __init__(self, x, y):
        self.loadSprites()
        self.currentFrameNum = 1

        self.x, self.y = x, y

        self.lastUpdate = 0

        self.currentFrame = self.roadRunnerFrames[0]



    def update(self, dt, inputs, fps):
        self.animate(dt)
        self.rect = self.currentFrame.get_rect()
        self.rect.center = (self.x, self.y)

    def render(self, screen):
        screen.blit(self.currentFrame, (self.rect.x, self.rect.y))

    def animate(self, dt):
        self.lastUpdate += dt

        if self.lastUpdate > 0.05:
            self.lastUpdate = 0
            self.currentFrameNum += 1
            self.currentFrame = self.roadRunnerFrames[(self.currentFrameNum % 3)]




    def loadSprites(self):
        roadRunnerSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/road runner.png')
        roadRunnerSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/road runner meta.json'), roadRunnerSpriteSheet)
        self.roadRunnerSprites = roadRunnerSpritesObject.getSprites()

        self.roadRunnerFrames = []
        for i in self.roadRunnerSprites:
            self.roadRunnerFrames.append(self.roadRunnerSprites[i])

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def update(self, dt, fps, scrollSpeed):
        self.rect.y += scrollSpeed * dt * fps
        if self.rect.y > 900:
            self.kill()
