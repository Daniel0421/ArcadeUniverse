import sys, pygame
from fighter import Fighter
pygame.init()

Screen_w = 1000
Screen_h = 600

screen = pygame.display.set_mode((Screen_w, Screen_h))
pygame.display.set_caption("Street Fighter")

Clock = pygame.time.Clock()
FPS = 60

intro_cnt = 0
last_cnt_update = pygame.time.get_ticks()
score = [0,0]
round_over = False
round_over_cooldown = 2000
game_start = True

warrior_size = 162
warrior_scale = 4
warrior_offset = [72, 56]
warrior_data = [warrior_size,warrior_scale,warrior_offset]
wizard_size = 250
wizard_scale = 3
wizard_offset = [112, 107]
wizard_data = [wizard_size,wizard_scale,wizard_offset]

bg = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

WARRIOR_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_STEPS = [8, 8, 1, 8, 8, 3, 7]

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

cnt_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x, y))
def draw_bg():
    scale_bg = pygame.transform.scale(bg,(Screen_w,Screen_h))
    screen.blit(scale_bg,(0, 0))

def draw_hb(health, x, y):
    ratio = health/100
    pygame.draw.rect(screen, BLACK, (x-5,y-5,410,40))
    pygame.draw.rect(screen, RED, (x,y,400,30))
    pygame.draw.rect(screen, YELLOW, (x,y,400*ratio,30))

fighter_1 = Fighter(1,200, 310, False, warrior_data, warrior_sheet, WARRIOR_STEPS)
fighter_2 = Fighter(2,700, 310, True,  wizard_data, wizard_sheet, WIZARD_STEPS)

run = True

while run:
    Clock.tick(FPS)
    draw_bg()

    draw_hb(fighter_1.health, 20, 20)
    draw_hb(fighter_2.health, 580, 20)

    draw_text("P1: "+str(score[0]),score_font, RED, 20,60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    if intro_cnt <= 0:
        fighter_1.move(Screen_w, Screen_h, screen, fighter_2, round_over)
        fighter_2.move(Screen_w, Screen_h, screen, fighter_1, round_over)
    else:
        draw_text(str(intro_cnt),cnt_font, RED, Screen_w/2, Screen_h/3)
        if(pygame.time.get_ticks() - last_cnt_update) >= 1000:
            intro_cnt -= 1
            last_cnt_update = pygame.time.get_ticks()
    # fighter_2.move()

    fighter_1.update()
    fighter_2.update()

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img,(360,150))
        if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
            round_over = False
            intro_cnt = 3
            fighter_1 = Fighter(1, 200, 310, False, warrior_data, warrior_sheet, WARRIOR_STEPS)
            fighter_2 = Fighter(2, 700, 310, True, wizard_data, wizard_sheet, WIZARD_STEPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

    pygame.display.update()
pygame.quit()