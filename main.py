import pygame
import math

#colors
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
silver = (197, 201, 199)

#newton_crade_settings
numberofcradles = 2
massofsphere = 20


#global_variables
height = 800
width = 1200
diameter = 50
len = 250
starty = 62
startx = width / 2  - numberofcradles * diameter / 2
angle = 0
angVel = 0
angAcc = 0
force = 0
gravity = 9.81
mass = 0.3
damping = 0.99
Pendulums = []


class Pendulum():
    def __init__(self, origin, angle, len):
        self.originx = origin[0]
        self.originy = origin[1]
        self.angle = angle
        self.updatePosition()
        self.len = len
        self.vel = 0
        self.acc = 0
        self.updatePendulum()
    def updatePosition(self):
        self.positionofcradlex = len * math.sin(self.angle) + self.originx - diameter/2
        self.positionofcradley = len * math.cos(self.angle) + self.originy - diameter/2
        self.collider = pygame.Rect(self.positionofcradlex, self.positionofcradley,diameter,diameter)
    def updatePendulum(self):
        self.arm = pygame.draw.aaline(screen, black, [self.originx, self.originy], [self.positionofcradlex + diameter/2, self.positionofcradley + diameter/2])
        self.bob = pygame.draw.ellipse(screen, silver, [self.positionofcradlex, self.positionofcradley, diameter, diameter], 0)
        #pygame.draw.rect(screen, black, self.collider, 2)

    def checkCollision(self):
        for j in Pendulums:
            if j != self:
                if self.collider.colliderect(j.collider):
                    if abs(self.vel) < 0.0002 and self.vel != 0:
                        if self.vel > 0:
                            self.angle -= 0.001
                        else:
                            self.angle += 0.001
                    if self.vel > 0:
                        self.angle -= 2.5*self.vel + abs(j.vel)
                    else:
                        self.angle += -2.5*self.vel - abs(j.vel)
                    self.updatePosition()
                    v1 = self.vel
                    v2 = j.vel
                    self.vel = (v1 + 2 * v2 - v1) / 2
                    j.vel = (v2 + 2 * v1 - v2) / 2
                    self.updatePosition()
                    j.updatePosition()
                    self.updatePendulum()
                    j.updatePendulum()


#Game
pygame.init()

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Newton Cradle")
screen.fill(white)
pdrag = False
clock = pygame.time.Clock()
active = True
time_elapsed_since_last_action = 0
collisions = []
counter = 0

for i in range(numberofcradles):
    Pendulums.append(Pendulum([startx + diameter * i, starty], 0, len))

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in Pendulums:
                    if i.bob.collidepoint(event.pos):
                        currPendelum = i
                        pdrag = True
                        mousex, mousey = event.pos
                        offset_x = i.bob.x - mousex
                        offset_y = i.bob.y - mousey
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pdrag = False
        elif event.type == pygame.MOUSEMOTION:
            if pdrag:
                mousex, mousey = event.pos
                xmove = mousex + offset_x
                currPendelum.angle = math.sin((xmove - currPendelum.originx)/len)
                currPendelum.updatePosition()

    dt = clock.tick()
    time_elapsed_since_last_action += dt


    if time_elapsed_since_last_action > 8:
        screen.fill(white)
        counter += 1
        for i in Pendulums:
            pygame.draw.line(screen, black, [50, 50], [1150, 50], 24)
            i.updatePendulum()
            i.angle += i.vel
            i.checkCollision()
            if counter == 5:
                i.vel *= damping
            force = gravity * math.sin(i.angle)
            i.acc = (-1 * force) / (len * 200 * mass)
            i.vel += i.acc
            i.updatePosition()
        pygame.display.flip()
        if counter == 5:
            counter = 0
        time_elapsed_since_last_action = 0

pygame.quit()