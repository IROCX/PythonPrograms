
# space invaders 1.0 game

# imports
import pygame
import os
import time
import random


pygame.font.init()
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('FX - Space Invaders')

# load images
RED_SPACESHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_red_small.png'))
BLUE_SPACESHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_blue_small.png'))
GREEN_SPACESHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_green_small.png'))

# player's ship
YELLOW_SPACESHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_yellow.png'))

# lasers
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(
    os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(
    os.path.join('assets', 'pixel_laser_yellow.png'))

# background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))


# ship character class
class Ship:

    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_laser(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 20
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.ship_img = YELLOW_SPACESHIP
        self.laser_img = YELLOW_LASER

        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_laser(self, velocity, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height()+10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.ship_img.get_height()+10, self.ship_img.get_width()*(self.health/self.max_health), 10))

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)


class Enemy(Ship):
    COLOR_MAP = {'red': (RED_SPACESHIP, RED_LASER),
                 'green': (GREEN_SPACESHIP, GREEN_LASER),
                 'blue': (BLUE_SPACESHIP, BLUE_LASER)
                 }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    offset_x = obj2.x-obj1.x
    offset_y = obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# mainloop

def main():
    run = True
    FPS = 60
    level = 0
    lives = 3
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont('comicsans', 30)
    lost_font = pygame.font.SysFont('comicsans', 50)
    player = Player(300, 630)
    player_velocity = 5

    laser_velocity = 5

    enemy_velocity = 2
    enemies = []
    wave_length = 5

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.fill((0, 0, 0))
        WIN.blit(BG, (0, 0))

        # draw scores n lives

        lives_label = main_font.render(f'Lives : {lives}', 1, (255, 0, 0))
        level_label = main_font.render(f'Level: {level}', 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH-level_label.get_width()-10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost == True:

            lost_label = lost_font.render("GAME OVER!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width() /
                                  2, HEIGHT/2 - lost_label.get_height()/2))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS*3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            lives = 3
            player.health = 100
            wave_length += 3
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100),
                              random.randrange(-1500, -100), random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x < WIDTH-player.get_width():
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y < HEIGHT-player.get_height()-20:
            player.y += player_velocity

        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_laser(laser_velocity, player)

            if random.randrange(0, 4*FPS) == 1:
                enemy.shoot()

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_laser(-laser_velocity, enemies)


def main_menu():

    title_font = pygame.font.SysFont('comicsans', 70)
    content_font = pygame.font.SysFont('comicsans', 40)

    run = True
    while run:

        WIN.blit(BG, (0, 0))
        title = title_font.render("FX Space Invaders 1.0", 1, (255, 255, 255))
        content = content_font.render(
            "Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title, (WIDTH/2 - title.get_width()/2, 300))
        WIN.blit(content, (WIDTH/2 - content.get_width()/2, 400))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


# mainloop call
main_menu()
