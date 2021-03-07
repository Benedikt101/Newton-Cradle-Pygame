import pygame
import math


#Main_Menu_Settings
width_Menu = 320
height_Menu = 450

#Newtoncradle-Settings
numberofpendulums = 5
height = 800
width = 1200
diameter = 50
len = 250
gravity = 9.81
mass = 0.3
damping = 0.999
draw_Hitbox = False

#global variables
starty = 62
startx = width / 2  - numberofpendulums * diameter / 2
angle = 0
force = 0
colors = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255), "black": (0, 0, 0), "grey": (227, 230, 225)}
Pendulums = []


class Pendulum():
    def __init__(self, origin, angle, len, screen):
        self.originx = origin[0]
        self.originy = origin[1]
        self.angle = angle
        self.len = len
        self.vel = 0
        self.acc = 0
        self.screen = screen
        self.updatePosition()
        self.updatePendulum()

    def updatePosition(self):
        self.positionofcradlex = len * math.sin(self.angle) + self.originx - diameter/2
        self.positionofcradley = len * math.cos(self.angle) + self.originy - diameter/2
        self.collider = pygame.Rect(self.positionofcradlex, self.positionofcradley,diameter,diameter)

    def updatePendulum(self):
        self.arm = pygame.draw.aaline(self.screen, colors.get("black"), [self.originx, self.originy], [self.positionofcradlex + diameter/2, self.positionofcradley + diameter/2])
        self.bob = pygame.draw.ellipse(self.screen, colors.get("grey"), [self.positionofcradlex, self.positionofcradley, diameter, diameter], 0)
        if draw_Hitbox:
            pygame.draw.rect(self.screen, colors.get("black"), self.collider, 2)

    def checkCollision(self):
        for j in Pendulums:
            if j != self:
                if self.collider.colliderect(j.collider):
                    self.angle += -self.vel
                    self.updatePosition()
                    v1 = self.vel
                    v2 = j.vel
                    self.vel = v2
                    j.vel = v1
                    self.updatePosition()
                    j.updatePosition()
                    self.updatePendulum()
                    j.updatePendulum()

def DrawText(size, msg, color, bckcolor):
    font = pygame.font.SysFont("arial", size)
    textsurface = font.render(msg, True, color, bckcolor)
    return textsurface

#Game
pygame.init()
def MainMenu():
    active = True
    screenMenu = pygame.display.set_mode((width_Menu,height_Menu))
    pygame.display.set_caption("Newton Cradle")
    rect1 = pygame.Rect(30, 230, 260, 50)
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect1.collidepoint(event.pos):
                        print("START")
                        active = False
                        NewtonCradleSimulation()
        screenMenu.fill(colors.get("white"))
        screenMenu.blit(DrawText(30, "Newtoncradle Simulator", colors.get("black"), None), (30, 100))
        pygame.draw.rect(screenMenu, colors.get("grey"), rect1 , 4)
        screenMenu.blit(DrawText(25, "Start", colors.get("black"), None), (135, 240))
        pygame.display.flip()


def NewtonCradleSimulation():
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Newton Cradle")
    clock = pygame.time.Clock()
    active = True

    pdrag = False
    time_elapsed_since_last_action = 0

    for i in range(numberofpendulums):
        Pendulums.append(Pendulum([startx + diameter * i, starty], 0, len, screen))

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
            screen.fill(colors.get("white"))
            for i in Pendulums:
                pygame.draw.line(screen, colors.get("black"), [50, 50], [1150, 50], 24)
                i.updatePendulum()
                i.angle += i.vel
                i.updatePosition()
                i.checkCollision()
                i.vel *= damping
                force = gravity * math.sin(i.angle)
                i.acc = (-1 * force) / (len * 200 * mass)
                i.vel += i.acc

            pygame.display.flip()
            time_elapsed_since_last_action = 0


MainMenu()

pygame.quit()