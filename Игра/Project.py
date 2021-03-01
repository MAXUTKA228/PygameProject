import pygame
import os
import sys
import random

pygame.init()

size = width, height = 600, 600
END = False
win_on = False
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
music1 = 'main_1.mp3'
music2 = 'main_2.mp3'
pygame.display.set_caption('64.0')
color_friend = random.choice(['red', 'blue', 'green', 'orange'])
start_time = 0
FPS = 60


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Player(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('squares/Tank.png'), (60, 60))

    def __init__(self, *group, enemy_group):
        super().__init__(*group)
        self.death = False
        self.enemy_group = enemy_group
        self.rect = self.image.get_rect()
        self.rect.x = 260
        self.rect.y = 250

    def rotate(self, diraction):
        if diraction == 'up':
            self.image = pygame.transform.rotate(Player.image, 0)
        if diraction == 'right':
            self.image = pygame.transform.rotate(Player.image, 270)
        if diraction == 'down':
            self.image = pygame.transform.rotate(Player.image, 180)
        if diraction == 'left':
            self.image = pygame.transform.rotate(Player.image, 90)

    def update(self):
        if pygame.sprite.spritecollideany(self, self.enemy_group):
            enemy = pygame.sprite.spritecollide(self, self.enemy_group, True)[0]
            if not enemy.god:
                self.death = True


class Bullet(pygame.sprite.Sprite):
    speed = 20
    image = pygame.transform.scale(load_image('squares/Bullet.png'), (100, 100))

    def __init__(self, *group, args, direction):
        super().__init__(*group)
        self.image = Bullet.image
        self.speed = Bullet.speed
        self.rect = self.image.get_rect()
        self.rect.x = args[0]
        self.rect.y = args[1]
        self.direction = direction

    def update(self):
        if self.direction == 'up':
            self.rect = self.rect.move(0, -self.speed)
        if self.direction == 'right':
            self.rect = self.rect.move(self.speed, 0)
        if self.direction == 'down':
            self.rect = self.rect.move(0, self.speed)
        if self.direction == 'left':
            self.rect = self.rect.move(-self.speed, 0)


class EndScreen(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('final_screen.jpg'), size)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = EndScreen.image
        self.rect = self.image.get_rect()
        self.rect.y = -height
        self.stop = False

    def update(self):
        if self.rect.y + height < height:
            self.rect = self.rect.move(0, 10)
        else:
            self.stop = True


class WinScreen(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('cong.jpg'), size)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = WinScreen.image
        self.rect = self.image.get_rect()
        self.rect.y = -height
        self.stop = False

    def update(self):
        if self.rect.y + height < height:
            self.rect = self.rect.move(0, 10)
        else:
            self.stop = True


class Enemy(pygame.sprite.Sprite):
    speed = 5
    image1 = pygame.transform.scale(load_image('squares/Blue square.png'), (60, 60))
    image2 = pygame.transform.scale(load_image('squares/Green square.png'), (60, 60))
    image3 = pygame.transform.scale(load_image('squares/Orange square.png'), (60, 60))
    image4 = pygame.transform.scale(load_image('squares/Red square.png'), (60, 60))
    args1 = ((-30, 245), 'right')
    args2 = ((255, -30), 'down')
    args3 = ((600, 237), 'left')
    args4 = ((255, 600), 'up')

    def __init__(self, *group, bullets):
        super().__init__(*group)
        self.god = False
        self.image = random.choice([Enemy.image1, Enemy.image2, Enemy.image3, Enemy.image4])
        if self.image == Enemy.image1 and color_friend == 'blue':
            self.god = True
        elif self.image == Enemy.image2 and color_friend == 'green':
            self.god = True
        elif self.image == Enemy.image3 and color_friend == 'orange':
            self.god = True
        elif self.image == Enemy.image4 and color_friend == 'red':
            self.god = True
        self.speed = Enemy.speed
        self.bullets = bullets
        self.rect = self.image.get_rect()
        self.args = random.choice([Enemy.args1, Enemy.args2, Enemy.args3, Enemy.args4])
        self.rect.x = self.args[0][0]
        self.rect.y = self.args[0][1]
        self.direction = self.args[-1]

    def update(self):
        global END
        if self.direction == 'right':
            self.rect = self.rect.move(self.speed, 0)
        elif self.direction == 'left':
            self.rect = self.rect.move(-self.speed, 0)
        elif self.direction == 'down':
            self.rect = self.rect.move(0, self.speed)
        elif self.direction == 'up':
            self.rect = self.rect.move(0, -self.speed)
        if pygame.sprite.spritecollideany(self, self.bullets):
            if not self.god:
                pygame.sprite.spritecollide(self, self.bullets, True)
                self.kill()
            else:
                END = True


def start_screen():
    intro_text = ["Нажмите любую клавишу для продолжения"]

    fon1 = pygame.transform.scale(load_image('Red.jpg'), size)
    fon2 = pygame.transform.scale(load_image('Blue.jpg'), size)
    fon3 = pygame.transform.scale(load_image('Green.jpg'), size)
    fon4 = pygame.transform.scale(load_image('Orange.jpg'), size)
    screen.blit(random.choice([fon1, fon2, fon3, fon4]), (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 77
        intro_rect.y = 275
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def run_game():
    global start_time, END
    pygame.mixer.music.load(random.choice([music1, music2]))
    pygame.mixer.music.play(-1)
    start_screen()
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    hero = Player(all_sprites, enemy_group=enemy_group)
    count = 0
    running = True
    end_on = False
    up = False
    right = False
    down = False
    left = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    bullet = Bullet(bullets, args=(242, 200), direction='up')
                    hero.rotate("up")
                elif event.key == pygame.K_s:
                    bullet = Bullet(bullets, args=(238, 258), direction='down')
                    hero.rotate("down")
                elif event.key == pygame.K_a:
                    bullet = Bullet(bullets, args=(212, 227), direction='left')
                    hero.rotate("left")
                elif event.key == pygame.K_d:
                    bullet = Bullet(bullets, args=(267, 230), direction='right')
                    hero.rotate("right")
        if count % 20 == 0:
            enemy = Enemy(all_sprites, bullets=bullets)
            enemy_group.add(enemy)
        count += 1
        if (pygame.time.get_ticks() - start_time) > 64000:
            win_on = True
            running = False
        elif hero.death:
            running = False
            end_on = True
        elif END:
            running = False
            end_on = True
        screen.fill(pygame.Color("black"))
        pygame.draw.rect(screen, pygame.Color(color_friend), (35, 35, 525, 525))
        pygame.draw.rect(screen, pygame.Color(color_friend), (0, 245, 35, 70))
        pygame.draw.rect(screen, pygame.Color(color_friend), (255, 0, 70, 35))
        pygame.draw.rect(screen, pygame.Color(color_friend), (560, 237, 40, 70))
        pygame.draw.rect(screen, pygame.Color(color_friend), (255, 560, 70, 40))
        all_sprites.draw(screen)
        bullets.draw(screen)
        bullets.update()
        all_sprites.update()
        clock.tick(FPS)
        pygame.display.flip()

    end_screen = EndScreen(all_sprites)
    pygame.mixer.music.load('lose.mp3')
    pygame.mixer.music.play(1)
    while end_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_on = False
            if pygame.key.get_pressed()[pygame.K_SPACE] and end_screen.stop:
                start_time = pygame.time.get_ticks()
                END = False
                run_game()
                return
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)

    win_screen = WinScreen(all_sprites)
    pygame.mixer.music.load('win.mp3')
    pygame.mixer.music.play(1)
    if win_on:
        while win_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    win_on = False
                if pygame.key.get_pressed()[pygame.K_SPACE] and win_screen.stop:
                    return
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
            clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    run_game()
