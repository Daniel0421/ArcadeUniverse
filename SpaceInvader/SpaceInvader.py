import pygame
import os
import time
import random

pygame.font.init()

# setup
pygame.init()
width = 750
height = 750
blinkInterval = 0.5
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invader")

# load assets (ships)
redShip = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
greenShip = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
blueShip = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# load assets (players)
yellowShip = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
yellowLaser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# load assets (laser)
redLaser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
greenLaser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
blueLaser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))

# load assets (background)
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (width, height))


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        screen.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, length):
        return not length >= self.y >= 0

    def collision(self, obj):
        return collide(obj, self)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.ship_laser = None
        self.lasers = []
        self.cool_time = 0

    def cooldown(self):
        if self.cool_time >= self.COOLDOWN:
            self.cool_time = 0
        elif self.cool_time > 0:
            self.cool_time += 1

    def shoot(self):
        if self.cool_time == 0:
            laser = Bullet(self.x, self.y, self.ship_laser)
            self.lasers.append(laser)
            self.cool_time = 1

    def draw(self, window):
        screen.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

    def move_laser(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


# inherit Ship class into Player class

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = yellowShip
        self.ship_laser = yellowLaser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.maxHealth = health

    def move_laser(self, velocity, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, screen):
        super().draw(screen)
        self.health_bar(screen)

    def health_bar(self,screen):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y+self.ship_img.get_height()+10, self.ship_img.get_width(),10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + self.ship_img.get_height()+10, self.ship_img.get_width()*(self.health/self.maxHealth),10))


class Enemy(Ship):
    # Classify images into colors
    colorMap = {
                "red": (redShip, redLaser),
                "green": (greenShip, greenLaser),
                "blue": (blueShip, blueLaser)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.ship_laser = self.colorMap[color]  # Calls images by color from attributes
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        if self.cool_time == 0:
            laser = Bullet(self.x-20, self.y, self.ship_laser)
            self.lasers.append(laser)
            self.cool_time = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    running = True
    fps = 60
    level = 0
    lives = 5
    player_velocity = 8
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    enemy = []
    wavelength = 5
    enemy_velocity = 2
    bullet_velocity = 6
    player = Player(300, 630)
    clock = pygame.time.Clock()
    lost = False
    lost_timer = 0

    # refreshing window (per fps)
    def redraw_window():
        screen.blit(background, (0, 0))

        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (width - level_label.get_width() - 10, 10))

        for bot in enemy:   # draw enemy ships
            bot.draw(screen)

        player.draw(screen)  # draw player ship
        if lost:
            lost_label = lost_font.render("Game Over", 1, (255, 255, 255))
            screen.blit(lost_label,(width/2-lost_label.get_width()/2,height/2-lives_label.get_height()))

        pygame.display.update()

    while running:
        clock.tick(fps)
        redraw_window()
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_timer += 1     # increment lost pause timer
        if lost:
            if lost_timer > fps * 3:   # if lost message shows for 3 seconds quit game
                running = False
            else:
                continue
        if len(enemy) == 0:  # increment level if all enemy ships are destroyed
            level += 1
            enemy_velocity += 0.1
            player_velocity += 0.5
            # if player.health != player.maxHealth:
            #    player.health += 0.5*player.health

            for i in range(wavelength):
                new_enemy = Enemy(random.randrange(50, width-100),random.randrange(-1500, -500),random.choice(["red", "green", "blue"]))
                enemy.append(new_enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # left
            if player.x - player_velocity - 10 > 0:
                player.x -= player_velocity
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # right
            if player.x + player_velocity + player.ship_img.get_width() + 5 < width:
                player.x += player_velocity
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # down
            if player.y + player_velocity + player.ship_img.get_height() + 20 + player_velocity < height:
                player.y += player_velocity
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # up
            if player.y - player_velocity - 10 > main_font.get_height():
                player.y -= player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        for ship in enemy[:]:
            ship.move(enemy_velocity)
            ship.move_laser(bullet_velocity, player)

            if random.randrange(0, 2 * 60) == 1:
                ship.shoot()
            if collide(ship, player):
                player.health -= 10
                enemy.remove(ship)
            elif ship.y + ship.ship_img.get_height() > height:
                lives -= 1
                enemy.remove(ship)

        player.move_laser(-bullet_velocity, enemy)


def main_menu():
    menu_font = pygame.font.SysFont("comic-sans", 60)
    lastVisibleTime = 0.5
    textVisible = True

    running = True
    while running:
        screen.blit(background, (0, 0))
        currentTime = time.time()
        if currentTime - lastVisibleTime >= blinkInterval:
            textVisible = not textVisible
            lastVisibleTime = currentTime
        if textVisible:
            menu_label = menu_font.render("Press any key to begin", 1, (255, 255, 255))
            screen.blit(menu_label, (width/2-menu_label.get_width()/2, height/2 - menu_label.get_height()))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


main_menu()
