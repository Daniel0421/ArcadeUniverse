import pygame
import os
import time
import random
pygame.font.init()

#setup
pygame.init()
width = 750
height = 750
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Invader")

#load assets (ships)
redShip = pygame.image.load(os.path.join("assets", "SpaceInvader", "pixel_ship_red_small.png"))
greenShip = pygame.image.load(os.path.join("assets", "SpaceInvader", "pixel_ship_green_small.png"))
blueShip = pygame.image.load(os.path.join("assets", "SpaceInvader", "pixel_ship_blue_small.png"))

#load assets (players)
yellowShip = pygame.image.load(os.path.join("assets", "SpaceInvader", "pixel_ship_yellow.png"))
yellowLaser = pygame.image.load(os.path.join("assets", "SpaceInvader", "pixel_laser_yellow.png"))

#load assests (laser)
redLaser = pygame.image.load(os.path.join("assets", "SpaceInvader", "pixel_laser_red.png"))
greenLaser = pygame.image.load(os.path.join("assets", "SpaceInvader", "pixel_laser_green.png"))
blueLaser = pygame.image.load(os.path.join("assets", "SpaceInvader", "pixel_laser_blue.png"))

#load assets (background)
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "SpaceInvader", "background-black.png")),(width,height))

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.ship_laser = None
        self.lasers = []
        self.cooltime = 0

    def draw(self, window):
        screen.blit(self.ship_img, (self.x,self.y))

#inherit Ship class into Player class
class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = yellowShip
        self.ship_laser = yellowLaser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.maxHealth = health

class Enemy(Ship):
    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.color = 

def main():
    running = True
    fps = 60
    level = 1
    lives = 5
    velocity = 10
    main_font = pygame.font.SysFont("comicsans",50)

    player = Player(300,650)

    clock = pygame.time.Clock()

    #refreshing window (per fps)
    def redraw_window():
        screen.blit(background,(0,0))

        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        screen.blit(lives_label, (10,10))
        screen.blit(level_label, (width-level_label.get_width()-10,10))

        player.draw(screen)

        pygame.display.update()

    while running: 
        clock.tick(fps)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: #left
            if player.x - velocity > 0: 
                player.x -= velocity
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: #right
            if player.x + velocity + player.ship_img.get_width() < width:
                player.x += velocity
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: #down
            if player.y + velocity + player.ship_img.get_height() < height:
                player.y += velocity
        if keys[pygame.K_w] or keys[pygame.K_UP]: #up
            if player.y - velocity > main_font.get_height():
                player.y -= velocity
 
main()
