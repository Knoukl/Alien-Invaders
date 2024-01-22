import pygame
import math
import random
import datetime

pygame.init()

# настройка размера окна и заднего фона
screen = pygame.display.set_mode((800, 800))
screen.blit(pygame.image.load('data/Fon.png'), (0, 0))
screen_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
screen_surface.set_alpha(128)
pygame.draw.rect(screen_surface, (0, 0, 0), pygame.Rect(0, 0, 800, 800))
screen.blit(screen_surface, (0, 0))

hp_bar_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
hp_bar_surface.set_alpha(140)
pygame.draw.rect(hp_bar_surface, (0, 0, 0), pygame.Rect(10, 10, 780, 30))
# иконка игры и название
pygame.display.set_caption('Alien Invaders')
pygame.display.set_icon(pygame.image.load('data/GameIconAlien.png'))

clock = pygame.time.Clock()
player_sprite = pygame.sprite.Group()
pulka_sprite = pygame.sprite.Group()
boss_pulka = pygame.sprite.Group()
boss_sprite = pygame.sprite.Group()
osminog_minions_sprite = pygame.sprite.Group()
menu = pygame.sprite.Group()
menu2 = pygame.sprite.Group()
restart = pygame.sprite.Group()
pygame.mixer.init()
# шрифт
font = pygame.font.Font('data/Fonts/minecraft.ttf', 28)
font2 = pygame.font.Font('data/Fonts/minecraft.ttf', 80)
text_surface = font2.render("Game Over", True, (255, 255, 255))
text_surface2 = font2.render("You Win", True, (255, 255, 255))
text_hp, coords_hp = font.render('HP:', True, (255, 255, 255)), (10, 650)
text_dmg, coords_dmg = font.render('DMG:', True, (255, 255, 255)), (10, 700)
text_ttldmg, coords_ttldmg = font.render('TOTAL DMG:', True, (255, 255, 255)), (10, 750)
# спрайты меню
game_name = [pygame.image.load('data/Cosmetic/name.png'), pygame.image.load('data/Cosmetic/name2.png')]
press_space = [pygame.image.load('data/Cosmetic/space.png'), pygame.image.load('data/Cosmetic/space2.png'),
               pygame.image.load('data/Cosmetic/space3.png'), pygame.image.load('data/Cosmetic/space4.png')]
alien_icon = pygame.image.load('data/Cosmetic/alien_icon.png')
pausel = [pygame.image.load('data/Cosmetic/pause.png'), pygame.image.load('data/Cosmetic/pause2.png')]
# спрайты для игрока
player_animation = [pygame.image.load('data/SpaceSheep/SpaceSheep10.png'),
                    pygame.image.load('data/SpaceSheep/SpaceSheep11.png'),
                    pygame.image.load('data/SpaceSheep/SpaceSheep12.png')]
player_animation_GET_DAMAGE = [[pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep10-1.png'),
                                pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep10-2.png'),
                                pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep10-3.png')],
                               [pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep11-1.png'),
                                pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep11-2.png'),
                                pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep11-3.png')],
                               [pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep12-1.png'),
                                pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep12-2.png'),
                                pygame.image.load('data/SpaceSheep/Get_Damage/SpaceSheep12-3.png')]]
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
osminog_minion_animation_GET_DAMAGE = \
    [pygame.image.load('data/Minion_sprites/Get_Damage_Osminog_Minions/Osminog_minion1_scaled_2x_pngcrushedINVERT.png'),
     pygame.image.load('data/Minion_sprites/Get_Damage_Osminog_Minions/Osminog_minion2_scaled_2x_pngcrushedINVERT.png'),
     pygame.image.load('data/Minion_sprites/Get_Damage_Osminog_Minions/Osminog_minion3_scaled_2x_pngcrushedINVERT.png'),
     pygame.image.load('data/Minion_sprites/Get_Damage_Osminog_Minions/Osminog_minion4_scaled_2x_pngcrushedINVERT.png')]
osminog_minion_animation_mirror = \
    [pygame.image.load('data/Minion_sprites/Osminog_minion1MIRROR_scaled_2x_pngcrushed.png'),
     pygame.image.load('data/Minion_sprites/Osminog_minion2MIRROR_scaled_2x_pngcrushed.png'),
     pygame.image.load('data/Minion_sprites/Osminog_minion3MIRROR_scaled_2x_pngcrushed.png'),
     pygame.image.load('data/Minion_sprites/Osminog_minion4MIRROR_scaled_2x_pngcrushed.png')]
osminog_minion_animation_mirror_GET_DAMAGE =  \
    [pygame.image.load('data/Minion_sprites/Get_Damage_Osminog_Minions/'
                       'Osminog_minion1MIRROR_scaled_2x_pngcrushedINVERT.png'),
     pygame.image.load('data/Minion_sprites/Get_Damage_Osminog_Minions/'
                       'Osminog_minion2MIRROR_scaled_2x_pngcrushedINVERT.png'),
     pygame.image.load('data/Minion_sprites/Get_Damage_Osminog_Minions/'
                       'Osminog_minion3MIRROR_scaled_2x_pngcrushedINVERT.png'),
     pygame.image.load('data/Minion_sprites/Get_Damage_Osminog_Minions/'
                       'Osminog_minion4MIRROR_scaled_2x_pngcrushedINVERT.png')]


class Player(pygame.sprite.Sprite):  # класс игрока (космический корабль)
    def __init__(self, x, y):
        super().__init__()
        self.image = player_animation[0]
        self.player_animation_count = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.step = 10

        self.hp = 1000
        self.get_damage = False

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
        if self.get_damage:
            if self.hp >= 50:
                self.hp -= 50
            self.get_damage = False


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

        self.hp = 5000
        self.damage_multi = len(osminog_minions_sprite) / 3
        self.damage = 250
        self.get_damage = False

        self.last_shot = 0

    def update(self):
        self.damage_multi = len(osminog_minions_sprite) / 3
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
            self.damage = int(50 * self.damage_multi)
            if self.damage < 50:
                self.damage = 50
            if self.hp - self.damage < 0:
                self.hp = 0
            else:
                self.hp -= self.damage
        self.get_damage = False

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 500:  # Проверяем, прошло ли 500 мс с момента последнего выстрела
            player = player_sprite.sprites()[0]  # Получаем объект игрока
            # Создаем новые пули
            bullet = Pulka_Osminog(self.rect.centerx, self.rect.centery - 70, player.rect.centerx, player.rect.centery)
            boss_pulka.add(bullet)
            self.last_shot = now  # Обновляем время последнего выстрела

    def draw_healthbar(self, pct):
        bar_length = 780
        bar_height = 30
        fill = (pct / 5000) * bar_length

        if int(fill) == 780:
            fill = 779
        procent = (780 - fill) / 780 * 100
        procent2 = int((procent * 255) / 100)
        color2 = (255, 0, 255 - procent2)

        fill_rect = pygame.Rect(10, 10, fill, bar_height)

        screen.blit(hp_bar_surface, (0, 0))
        if color2[2] > 0:
            pygame.draw.rect(screen, color2, fill_rect)


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
        self.radius = radius

        self.damage_multi = len(osminog_minions_sprite) / 3
        self.get_damage = False

    def update(self):
        self.damage_multi = len(osminog_minions_sprite) / 3
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
        if not self.hp:
            self.kill()


class menu_game_name(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_name[0]

        self.animation_count = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = [48, 100]
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 450:  # Прошло 100 миллисекунд с момента последнего обновления
            self.animation_count = (self.animation_count + 1) % len(game_name)
            self.image = game_name[self.animation_count]
            self.last_update = now


class press_to_play(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = press_space[0]
        self.space_count = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = [142, 600]
        self.last_update = pygame.time.get_ticks()
        self.menu_flag = False
        self.key_down_flag = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:  # Прошло 100 миллисекунд с момента последнего обновления
            self.space_count = (self.space_count + 1) % len(press_space)
            self.image = press_space[self.space_count]
            self.last_update = now


class pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pause_count = 0
        self.image = pausel[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [245, 200]
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 200:  # Прошло 100 миллисекунд с момента последнего обновления
            self.pause_count = (self.pause_count + 1) % len(pausel)
            self.image = pausel[self.pause_count]
            self.last_update = now


class MusicPlayer:
    def __init__(self):
        self.current_music = None

    def play_music(self, music_file):
        if music_file != self.current_music:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)
            self.current_music = music_file

    def get_current_music(self):
        return self.current_music


# добавление музыки
play_muz = MusicPlayer()
play_muz.play_music('data/Music/music.ogg')
# добавление спрайтов в отдельные группы

player_sprite.add(Player(350, 650))
boss_sprite.add(Osminog(198, 90))
restart.add(press_to_play())
menu.add(menu_game_name())
menu.add(press_to_play())
menu2.add(pause())
menu2.add(press_to_play())
press_to_play_sprite = press_to_play()


radius = 230
num_minions = 15
angle_step = 2*math.pi / num_minions
for i in range(num_minions):
    angle = i * angle_step
    dx = radius * math.cos(angle)
    dy = radius * math.sin(angle)
    for osminog in boss_sprite:
        minion = Osminog_minion(osminog.rect.x, osminog.rect.y, angle)
        osminog_minions_sprite.add(minion)


# Движения боссов
return_osminog = False

ok = 1
count = 0
count2 = 0
ps = True
flagg = False
start = False
game_over_win = True
game_over_lose = True
spawn_delay = 500
current_time = pygame.time.get_ticks()
last_spawn_time = pygame.time.get_ticks()

total_dmg = 0

file = open('data/last_score.txt', mode='r+')
s = file.readlines()
file.close()
running = True
while running:
    clock.tick(160)
    restart.update()
    screen.blit(pygame.image.load('data/Fon.png'), (0, 0))
    screen.blit(screen_surface, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # стрельба с космического корабля
        elif pygame.key.get_pressed()[pygame.K_UP]:
            current_time = pygame.time.get_ticks()
            if current_time - last_spawn_time > spawn_delay:
                pygame.mixer.Channel(0).set_volume(0.1)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/Music/shot.mp3'))
                for player in player_sprite:
                    pulka_sprite.add(Pulka(player.rect.x + 14))
                    pulka_sprite.add(Pulka(player.rect.x + 80))
                    flagg = True
                    last_spawn_time = current_time
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over_lose and game_over_win:
                    start = not start
                    ps = False

    # обновление спрайтов и их отрисовывание
    if not start:
        current_music = play_muz.get_current_music()
        if current_music != 'data/Music/music.ogg':
            play_muz.play_music("data/Music/music.ogg")
        if ps:
            menu.update()
            screen.blit(alien_icon, (272, 250))
            menu.draw(screen)
        else:
            menu2.update()
            menu2.draw(screen)
    elif start and game_over_lose and game_over_win:
        current_music = play_muz.get_current_music()
        if current_music != 'data/Music/music2.ogg':
            play_muz.play_music("data/Music/music2.ogg")
        for boss in boss_sprite:
            boss.draw_healthbar(boss.hp)
        screen.blit(text_hp, coords_hp)
        screen.blit(text_dmg, coords_dmg)
        screen.blit(text_ttldmg, coords_ttldmg)
        screen.blit(font.render(f'{total_dmg}', True, (255, 255, 255)), (195, 750))
        for player in player_sprite:
            screen.blit(font.render(f'{player.hp}', True, (255, 255, 255)), (60, 650))
        for osminog in boss_sprite:
            screen.blit(font.render(f'{boss.damage}', True, (255, 255, 255)), (80, 700))
            text_bosshp = font.render(f'{osminog.hp}', True, (0, 255, 175))
            coords_bosshp = ((400 - text_bosshp.get_size()[0] // 2), 12)
            screen.blit(text_bosshp, coords_bosshp)
        # стрельба босса осминога
        [boss.shoot() for boss in boss_sprite]
        # регистрация попаданий
        for pulka in pulka_sprite:
            for osminog in boss_sprite:
                if pygame.sprite.collide_mask(pulka, osminog):
                    pygame.mixer.Channel(0).set_volume(0.1)
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/Music/reg.mp3'))
                    pulka.kill()
                    osminog.get_damage = True
                    if osminog.hp - osminog.damage < 0:
                        total_dmg += osminog.hp
                    else:
                        total_dmg += osminog.damage
        for pulka in pulka_sprite:
            for osminog_minion in osminog_minions_sprite:
                if pygame.sprite.collide_mask(pulka, osminog_minion):
                    pygame.mixer.Channel(3).set_volume(0.1)
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('data/Music/reg.mp3'))
                    pulka.kill()
                    osminog_minion.get_damage = True
                    total_dmg += 50
        for pulka in boss_pulka:
            for player in player_sprite:
                if pygame.sprite.collide_mask(pulka, player):
                    pygame.mixer.Channel(1).set_volume(0.1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/Music/reg.mp3'))
                    pulka.kill()
                    player.get_damage = True
        # подсвечивание миньонов осминога, если в них попали
        for minion in osminog_minions_sprite:
            if minion.get_damage:
                if minion.rect.x <= minion.boss_x:
                    minion.osminog_minion_animation_count = (minion.osminog_minion_animation_count + 1) \
                                                            % len(osminog_minion_animation)
                    minion.image = osminog_minion_animation_mirror_GET_DAMAGE[minion.osminog_minion_animation_count]
                else:
                    minion.osminog_minion_animation_count = (minion.osminog_minion_animation_count + 1) \
                                                            % len(osminog_minion_animation)
                    minion.image = osminog_minion_animation_GET_DAMAGE[minion.osminog_minion_animation_count]

        for player in player_sprite:
            if player.get_damage:
                player.player_animation_count = (player.player_animation_count + 1) % len(player_animation)
                for image in player_animation_GET_DAMAGE[player.player_animation_count]:
                    player.image = image
        for osminog in boss_sprite:
            if osminog.hp == 0:
                game_over_lose = False

        for playerok in player_sprite:
            if playerok.hp == 0:
                game_over_win = False
        player_sprite.update()
        pulka_sprite.update()
        pulka_sprite.draw(screen)
        boss_sprite.update()
        boss_sprite.draw(screen)
        player_sprite.draw(screen)
        osminog_minions_sprite.update()
        osminog_minions_sprite.draw(screen)
        boss_pulka.update()
        boss_pulka.draw(screen)
    elif not game_over_lose and start:
        screen.blit(text_surface2, (400 - text_surface2.get_size()[0] // 2 + 5, 200))
        play_muz.play_music('data/Music/game_end.mp3')
        restart.draw(screen)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                log_time = datetime.datetime.now()
                s = [str(log_time)[:-7] + '\n', f'SpaceSheep HP saved: {player.hp}' +
                     '\n', f'Total DMG score: {total_dmg}' + '\n', ' ' + '\n'] + s
                with open('data/last_score.txt', 'w') as file:
                    file.writelines(s)
                file.close()
                exec(open(r'restarter.py').read())
                pygame.quit()

    elif not game_over_win and start:
        screen.blit(text_surface, (400 - text_surface.get_size()[0] // 2 + 5, 200))
        play_muz.play_music("data/Music/game_end.mp3")
        restart.draw(screen)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                log_time = datetime.datetime.now()
                s = [str(log_time)[:-7] + '\n', f'SpaceSheep HP saved: {player.hp}' +
                     '\n', f'Total DMG score: {total_dmg}' + '\n', ' ' + '\n'] + s
                with open('data/last_score.txt', 'w') as file:
                    file.writelines(s)
                file.close()
                exec(open(r'restarter.py').read())
                pygame.quit()

    for osminog in boss_sprite:
        if osminog.hp == 0:
            hp_otris = font.render(f'SpaceSheep HP saved: {player.hp}', True, (255, 255, 255))
            dmg_otris = font.render(f'Total DMG score: {total_dmg}', True, (255, 255, 255))
            screen.blit(hp_otris, (400 - hp_otris.get_size()[0] // 2 + 5, 380))
            screen.blit(dmg_otris, (400 - dmg_otris.get_size()[0] // 2 + 5, 430))
    pygame.display.update()
    pygame.display.update()
pygame.quit()
