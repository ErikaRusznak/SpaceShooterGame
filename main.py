import pygame
import os
import time
import random
from ship import Ship

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load the images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Load in the lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BACKGROUND = pygame.transform.scale(BG, (WIDTH, HEIGHT))


class PlayerShip(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class EnemyShip(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity  # moving the ship down


def main():
    run = True
    FPS = 60  # the higher the number, the faster the game is going to run
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 40)

    enemies = []
    wave_length = 0
    enemy_velocity = 1

    player_velocity = 5  # lower fps (clock speed) -> higher velocity

    player = PlayerShip(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        WINDOW.blit(BACKGROUND, (0, 0))
        # in pygame 0,0 is starting in the top left of the window

        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if len(enemies) == 0:  # no more enemies on the screen
            level += 1
            wave_length += 5
            for i in range(wave_length):
                # we want to spawn them all here, at the same time but at diff heights so they won't come
                # down in the same row
                # we are going to put them at different heights and diff x values
                # (heights that are not in our created window)
                enemy = EnemyShip(random.randrange(50, WIDTH - 100), random.randrange(-1000, -100),
                                  random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():  # 60 times per seconds check if an event has occurred
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()  # returns a dict of all the keys and tell us whether they are pressed or not
        if keys[pygame.K_a] and player.x - player_velocity > 0:  # left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH:  # right
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0:  # up
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() < HEIGHT:  # down
            player.y += player_velocity

        for enemy in enemies:
            enemy.move(enemy_velocity)

        redraw_window()


main()
