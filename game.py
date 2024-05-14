import pygame
import os
import time
import random

#setup
pygame.init()
screen = pygame.display.set_mode((750,750))
pygame.display.set_caption("Space Invader")

#load assets (ships)
redShip = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
greenShip = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
blueShip = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

#load assets (players)
yellowShip = pygame.image.load(os.path.join("assets","pixe_ship_yellow.png"))

#load assests (laser)
redLazer = pygame.image.load(os.path.join("assets","pixel_lazer_red.png"))
greenLazer = pygame.image.load(os.path.join("assets","pixel_lazer_green.png"))
blueLazer = pygame.image.load(os.path.join("assets","pixel_lazer_blue.png"))

#load assets (background)
background = pygame.image.load(os.path.join("assets","background-black.png"))