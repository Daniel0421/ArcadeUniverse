import pygame
import os
import time
import random

#setup
pygame.init()
screen = pygame.display.set_mode((750,750))
pygame.display.set_caption("Space Invader")

#load assets (ships)
redShip = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
greenShip = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
blueShip = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

#load assets (players)
yellowShip = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

#load assests (laser)
redLaser = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
greenLaser = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
blueLaser = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))

#load assets (background)
background = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(750,750))

def main():
    running = True
    fps = 60
    level = 1
    lives = 5
    clock = pygame.time.Clock()

    def redraw_window():
        screen.blit(background,(0,0))
        pygame.display.update()

    while running: 
        clock.tick(fps)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
main()
