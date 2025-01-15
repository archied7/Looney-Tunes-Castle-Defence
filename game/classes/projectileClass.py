import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, targetX, targetY, targetSpeed, targetStopX, image, damage):
        pygame.sprite.Sprite.__init__(self)
        angle = 60
        self.theta = math.radians(angle)

        self.x, self.y = x, y
        if targetX - targetSpeed*20 >= targetStopX:
            newX = targetX - targetSpeed*20
        else:
            newX = targetStopX-20

        self.targetX, self.targetY = newX, targetY
        self.image = image
        self.rect = self.image.get_rect()
        self.damage = damage
        self.time = 0

        self.dx = self.targetX - self.x
        self.dy = self.y - self.targetY

        self.calculateInitialVel()

    def update(self, dt, fps):

        if self.rect.y > 1000 or self.rect.x > 1500:
            self.kill()
        else:
            self.time += 1 * dt * fps
            pos = self.calculatePath(self.time)
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        
        

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def calculatePath(self, time):
        self.vx = math.cos(self.theta) * self.vi
        self.vy = math.sin(self.theta) * self.vi

        distX = self.vx * time
        distY = (self.vy * time) + ((-9.8 * (time)**2) / 2)

        x = round(distX + self.x)
        y = round(self.y - distY)

        return (x,y)

    def calculateInitialVel(self):
        g = 9.8
        self.vi = math.sqrt((g * self.dx**2) / (2 * (self.dx * math.sin(self.theta) * math.cos(self.theta) - self.dy * math.cos(self.theta)**2)))



    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprites, x, y, damage, isEnemy ,targetX=None, targetY=None, animate=False):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x,y)
        self.image = self.sprites[0]
        self.lastUpdate = 0
        self.currentFrameNum = 1
        self.animate = animate
        self.isEnemy = isEnemy
        self.damage = damage

        if not isEnemy:
            dx = targetX - x
            dy = targetY - y
            magnitude = math.sqrt(dx**2 + dy**2)
            self.dx = dx/magnitude
            self.dy = dy/magnitude

    def update(self, dt, fps):
        if self.animate:
            self.lastUpdate += dt
            
            if self.lastUpdate > 0.1:
                self.lastUpdate = 0
                self.currentFrameNum += 1
                self.image = self.sprites[(self.currentFrameNum % 2)]

        if self.isEnemy:
            self.rect.x -= 20 * dt * fps

        else:
            self.rect.x += self.dx * 45 * dt * fps
            self.rect.y += self.dy * 45 * dt * fps
        
        if self.rect.x > 2000 or self.rect.y > 1000:
            self.kill()
