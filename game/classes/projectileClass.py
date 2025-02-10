import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, targetX: int, targetY: int, targetSpeed: float, targetStopX: int, image: pygame.Surface, damage: int) -> None:
        #intialise sprite
        pygame.sprite.Sprite.__init__(self)

        #set intial angle
        angle = 60
        #convert to radians
        self.theta = math.radians(angle)

        self.x, self.y = x, y

        #adjust for target movement
        if targetX - targetSpeed*25 >= targetStopX:
            newX = targetX - targetSpeed*25 + 10
        else:
            newX = targetStopX + 10

        #set variables
        self.targetX, self.targetY = newX, targetY
        self.image = image
        self.rect = self.image.get_rect()
        self.damage = damage
        self.time = 0

        self.dx = self.targetX - self.x
        self.dy = self.y - self.targetY

        #set initial velocity
        self.calculateInitialVel()

    def update(self, dt: float, fps: int) -> None:
        #check projectile is still within screen
        if self.rect.y > 1000 or self.rect.x > 1500:
            self.kill()
        else:
            #update projectile's position
            self.time += 0.75 * dt * fps
            pos = self.calculatePath(self.time)
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        
        

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def calculatePath(self, time: float) -> tuple:
        #calculate the x and y vectors
        self.vx = math.cos(self.theta) * self.vi
        self.vy = math.sin(self.theta) * self.vi

        #calculate distance travelled in x and y
        distX = self.vx * time
        distY = (self.vy * time) + ((-9.8 * (time)**2) / 2)

        #calculate new x and y position
        x = round(distX + self.x)
        y = round(self.y - distY)

        return (x,y)

    def calculateInitialVel(self) -> None: 
        g = 9.8
        self.vi = math.sqrt((g * self.dx**2) / (2 * (self.dx * math.sin(self.theta) * math.cos(self.theta) - self.dy * math.cos(self.theta)**2)))



    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprites: list, x: int, y: int, damage: int, isEnemy: bool, targetX: int=None, targetY: int=None, animate: bool=False) -> None:
        #initialise sprite
        pygame.sprite.Sprite.__init__(self)

        #set variables
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
            #calculate x and y direction vectors
            #if hero
            dx = targetX - x
            dy = targetY - y

            magnitude = math.sqrt(dx**2 + dy**2)

            self.dx = dx/magnitude
            self.dy = dy/magnitude

    def update(self, dt: float, fps: int) -> None:
        if self.animate:
            #updates projectile image
            self.lastUpdate += dt
            
            if self.lastUpdate > 0.1:
                self.lastUpdate = 0
                self.currentFrameNum += 1
                self.image = self.sprites[(self.currentFrameNum % 2)]

        if self.isEnemy:
            #moves projectile left
            #if enemy projectile
            self.rect.x -= 20 * dt * fps

        else:
            #moves projectile along vector
            #if hero projectile
            self.rect.x += self.dx * 45 * dt * fps
            self.rect.y += self.dy * 45 * dt * fps
        
        #checks if bullet is still within screen
        if self.rect.x > 2000 or self.rect.y > 1000:
            self.kill()
