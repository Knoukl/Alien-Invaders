import pygame
import math
import random

pygame.init()

# настройка размера окна и заднего фона
screen = pygame.display.set_mode((800, 800))
screen.blit(pygame.image.load('data/Fon.png'), (0, 0))
screen_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
screen_surface.set_alpha(128)
pygame.draw.rect(screen_surface, (0, 0, 0), pygame.Rect(0, 0, 800, 800))
screen.blit(screen_surface, (0, 0))

pygame.display.set_caption('Alien Invaders')
pygame.display.set_icon(pygame.image.load('data/GameIconAlien.png'))

clock = pygame.time.Clock()
player_sprite = pygame.sprite.Group()
pulka_sprite = pygame.sprite.Group()
boss_pulka = pygame.sprite.Group()
boss_sprite = pygame.sprite.Group()
osminog_minions_sprite = pygame.sprite.Group()
# спрайты для игрока
player_animation = [pygame.image.load('data/SpaceSheep/SpaceSheep10.png'),
                    pygame.image.load('data/SpaceSheep/SpaceSheep11.png'),
                    pygame.image.load('data/SpaceSheep/SpaceSheep12.png')]
# спрайты для пуль игрока
pulka_animation = [pygame.image.load('data/Pulka_SpaceSheep/PulkaLeftTEST.png'),
                   pygame.image.load('data/Pulka_SpaceSheep/PulkaRightTEST.png')]
# спрайты босса осминога
boss_osminog_animation = [pygame.image.load('data/Boss_sprites/Boss_Osminog.png').convert_alpha()]
boss_osminog_animation_GET_DAMAGE = [pygame.image.load('data/Boss_sprites/Get_Damage_Osminog/Boss_Osminog_Invert1.png'),
                                     pygame.image.load('data/Boss_sprites/Get_Damage_Osminog/Boss_Osminog_Invert2.png'),
                                     pygame.image.load('data/Boss_sprites/Get_Damage_Osminog/Boss_Osminog_Invert3.png'),
                                     pygame.image.load('data/Boss_sprites/Get_Damage_Osminog/Boss_Osminog_Invert4.png'),
                                     pygame.image.load('data/Boss_sprites/Get_Damage_Osminog/Boss_Osminog_Invert5.png'),
                                     pygame.image.load('data/Boss_sprites/Get_Damage_Osminog/Boss_Osminog_Invert6.png'),
                                     pygame.image.load('data/Boss_sprites/Get_Damage_Osminog/Boss_Osminog_Invert7.png')]
# спрайты миньонов босса осминога
osminog_minion_animation = [pygame.image.load('data/Minion_sprites/Osminog_minion1_scaled_2x_pngcrushed.png'),
                            pygame.image.load('data/Minion_sprites/Osminog_minion2_scaled_2x_pngcrushed.png'),
                            pygame.image.load('data/Minion_sprites/Osminog_minion3_scaled_2x_pngcrushed.png'),
                            pygame.image.load('data/Minion_sprites/Osminog_minion4_scaled_2x_pngcrushed.png')]
osminog_minion_animation_mirror = \
    [pygame.image.load('data/Minion_sprites/Osminog_minion1MIRROR_scaled_2x_pngcrushed.png'),
     pygame.image.load('data/Minion_sprites/Osminog_minion2MIRROR_scaled_2x_pngcrushed.png'),
     pygame.image.load('data/Minion_sprites/Osminog_minion3MIRROR_scaled_2x_pngcrushed.png'),
     pygame.image.load('data/Minion_sprites/Osminog_minion4MIRROR_scaled_2x_pngcrushed.png')]


class Player(pygame.sprite.Sprite):  # класс игрока (космический корабль)
    def __init__(self, x, y):
        super().__init__()
        self.image = player_animation[0]
        self.player_animation_count = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.hp = 1000
        self.step = 10

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:  # Прошло 100 миллисекунд с момента последнего обновления
            self.player_animation_count = (self.player_animation_count + 1) % len(player_animation)
            self.image = player_animation[self.player_animation_count]
            self.last_update = now
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.step
        elif keys[pygame.K_RIGHT]:
            if self.rect.x < 700:
                self.rect.x += self.step


class Pulka(pygame.sprite.Sprite):  # класс пуль игрока
    def __init__(self, x):
        super().__init__()
        self.image = pulka_animation[0]
        self.pulka_animation_count = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 666)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 70:
            self.pulka_animation_count = (self.pulka_animation_count + 1) % len(pulka_animation)
            self.image = pulka_animation[self.pulka_animation_count]
            self.last_update = now
        if flagg:
            if self.rect.y > -14:
                self.rect.y -= 10
            else:
                pulka_sprite.sprites()[0].kill()


class Osminog(pygame.sprite.Sprite):  # класс босса осминога
    def __init__(self, x, y):
        super().__init__()
        self.image = boss_osminog_animation[0]
        self.boss_osminog_animation_GET_DAMAGE_count = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.last_update = pygame.time.get_ticks()

        self.direction = 1
        self.step = 1

        self.damage = 50
        self.hp = 10000
        self.damage_multi = len(osminog_minions_sprite) / 6
        self.get_damage = False

        self.last_shot = 0

    def update(self):
        self.damage_multi = len(osminog_minions_sprite) / 6
        self.image = boss_osminog_animation[0]
        now = pygame.time.get_ticks()
        if now - self.last_update > 1:
            if self.rect.x > 330:
                self.direction = -1
            elif self.rect.x < 60:
                self.direction = 1
            self.rect.x += self.step * self.direction
            self.last_update = now
        if self.get_damage:
            for image in boss_osminog_animation_GET_DAMAGE:
                self.image = image
            self.damage = 50 * self.damage_multi
            if self.damage < 50:
                self.damage = 50
            self.hp -= self.damage
            print(self.hp)
        self.get_damage = False

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 500:  # Проверяем, прошло ли 400 мс с момента последнего выстрела
            player = player_sprite.sprites()[0]  # Получаем объект игрока
            # Создаем новые пули
            bullet = Pulka_Osminog(self.rect.centerx, self.rect.centery - 70, player.rect.centerx, player.rect.centery)
            boss_pulka.add(bullet)
            self.last_shot = now  # Обновляем время последнего выстрела

class Pulka_Osminog(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.image.load('data\Pulka2.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.target_x = target_x + random.randint(1, 5)
        self.target_y = target_y + random.randint(1, 5)
        self.speed = 7

    def update(self):
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            self.target_x = self.rect.x + dx * self.speed
            self.target_y = self.rect.y + dy * self.speed
        if (self.rect.centerx > 810 or self.rect.centery > 810) or self.rect.centerx < -10:
            boss_pulka.sprites()[0].kill()


class Osminog_minion(pygame.sprite.Sprite):  # класс миньонов босса осминога
    def __init__(self, x, y, angle=0, radius=230):
        super().__init__()
        self.image = osminog_minion_animation[0]

        self.rect = self.image.get_rect()
        self.boss_x = x
        self.boss_y = y

        self.last_update = pygame.time.get_ticks()
        self.osminog_minion_animation_count = 0

        self.step = 1
        self.hp = 300
        self.angle = angle
        self.radius = 230

        self.damage_multi = len(osminog_minions_sprite) / 6
        self.get_damage = False

    def update(self):
        self.damage_multi = len(osminog_minions_sprite) / 6
        now = pygame.time.get_ticks()
        if now - self.last_update > 300:
            if self.rect.x <= self.boss_x:
                self.osminog_minion_animation_count = (self.osminog_minion_animation_count + 1) \
                                                      % len(osminog_minion_animation)
                self.image = osminog_minion_animation_mirror[self.osminog_minion_animation_count]
                self.last_update = now
            else:
                self.osminog_minion_animation_count = (self.osminog_minion_animation_count + 1) \
                                                  % len(osminog_minion_animation)
                self.image = osminog_minion_animation[self.osminog_minion_animation_count]
                self.last_update = now
        dx = self.radius * math.cos(self.angle)
        dy = self.radius * math.sin(self.angle)
        for osminog in boss_sprite:
            self.boss_x = osminog.rect.centerx
            self.boss_y = osminog.rect.centery
        self.rect.x = self.boss_x + dx - 32
        self.rect.y = self.boss_y + dy - 10
        self.angle += 0.03  # Изменяем угол поворота
        if self.get_damage:

            self.hp -= 50
            self.get_damage = False
            print(self.hp)
        if not self.hp:
            print(self.hp)
            self.kill()


# добавление спрайтов в отдельные группы

player_sprite.add(Player(350, 650))
boss_sprite.add(Osminog(198, 50))

radius = 230
num_minions = 20
angle_step = 2*math.pi / num_minions
for i in range(num_minions):
    angle = i * angle_step
    dx = radius * math.cos(angle)
    dy = radius * math.sin(angle)
    for osminog in boss_sprite:
        minion = Osminog_minion(osminog.rect.x, osminog.rect.y, angle)
        osminog_minions_sprite.add(minion)
print(len(osminog_minions_sprite))



# Движения боссов
return_osminog = False

ok = 1
flagg = False
spawn_delay = 500
current_time = pygame.time.get_ticks()
last_spawn_time = pygame.time.get_ticks()

# Получение урона
osminog_get_damage = False


running = True
while running:
    clock.tick(60)
    screen.blit(pygame.image.load('data/Fon.png'), (0, 0))
    screen.blit(screen_surface, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif pygame.key.get_pressed()[pygame.K_UP]:
            current_time = pygame.time.get_ticks()
            if current_time - last_spawn_time > spawn_delay:
                for player in player_sprite:
                    pulka_sprite.add(Pulka(player.rect.x + 14))
                    pulka_sprite.add(Pulka(player.rect.x + 80))
                    flagg = True
                    last_spawn_time = current_time

    [boss.shoot() for boss in boss_sprite]

    # регистрация попаданий
    for pulka in pulka_sprite:
        for osminog in boss_sprite:
            if pygame.sprite.collide_mask(pulka, osminog):
                pulka.kill()
                osminog.get_damage = True
    for pulka in pulka_sprite:
        for osminog_minion in osminog_minions_sprite:
            if pygame.sprite.collide_mask(pulka, osminog_minion):
                pulka.kill()
                osminog_minion.get_damage = True

    # обновление спрайтов и их отрисовывание
    player_sprite.update()
    pulka_sprite.update()
    pulka_sprite.draw(screen)
    boss_sprite.update()
    boss_sprite.draw(screen)
    player_sprite.draw(screen)
    osminog_minions_sprite.update()
    osminog_minions_sprite.draw(screen)
    osminog_minions_sprite.draw(screen)
    boss_pulka.update()
    boss_pulka.draw(screen)
    pygame.display.update()
    pygame.display.update()

pygame.quit()