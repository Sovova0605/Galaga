import pygame
import random
import sys
import sqlite3


bd = sqlite3.connect('Game.db')
cur = bd.cursor()
cur.execute('''create table if not exists Score(score integer)''')
pygame.init()
win = pygame.display.set_mode((500, 530))
screen = pygame.Surface((500, 500))
pygame.display.set_caption('Galaga')
# Фон
bg = pygame.image.load('bg.png')
bg_rect = bg.get_rect()
# Счёт 
score = 0
# Лучший результат 
best_score = 0
# Строка состояния 
info_string = pygame.Surface((500, 30))
# Жизни игрока 
hp = 3
# Жизни врага 
en_hp = 1
# Пременная увелечения скорости снаряда
scor = 1
# Шаг врага вниз 
move = 15
# Спрайты 
player_2 = pygame.image.load('idle.png')
weapon = pygame.image.load('snar.png')
enemy = pygame.image.load('enemy.png')
station = pygame.image.load('station.png')
enemy_2 = pygame.image.load('enemy_2.png')
class Player:
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.transform.scale(player_2, (38, 60))
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        screen.blit(self.bitmap,(self.x,self.y))


class Weapon:
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.transform.scale(weapon, (5, 15))
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        screen.blit(self.bitmap,(self.x,self.y))


class Enemy:
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.transform.scale(enemy, (38, 60))
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        screen.blit(self.bitmap,(self.x,self.y))


class Enemy_2:
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.transform.scale(enemy_2, (38, 60))
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        screen.blit(self.bitmap,(self.x,self.y))


class Station:
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.transform.scale(station, (90, 80))
        self.bitmap.set_colorkey((0, 0, 0))

    def render(self):
        screen.blit(self.bitmap,(self.x,self.y))

        
def Intersect(x1, x2, y1, y2, db1, db2):
    if (x1 > x2 - db1) and (x1 < x2 + db2) and (y1 > y2 - db1) and (y1 < y2 + db2):
        return 1
    else:
        return 0

class Menu:
    def __init__(self, punkts = [120, 140, u'Punkt', (250, 250, 30), (250, 30, 250), 0]):
        self.punkts = punkts

    def render(self, a, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                a.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                a.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        global flag
        flag = 0
        done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            info_string.blit(bg, bg_rect)
            screen.blit(bg, bg_rect)
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 55 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        done = False
                        game.menu()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                        flag = 0
                    elif punkt == 1:
                        done = False
                        flag = 1
                    elif punkt == 2:
                        pygame.quit()
                        sys.exit()
            win.blit(info_string, (0, 0)) 
            win.blit(screen, (0, 30))
            pygame.display.flip()


class GameOver:
    def __init__(self, punkt_2 = [120, 140, u'Punkt', (250, 250, 30), (250, 30, 250), 0]):
        self.punkt_2 = punkt_2

    def render(self, a, font, num_punkt):
        for i in self.punkt_2:
            if num_punkt == i[5]:
                a.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                a.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def gameOver(self):
        done = True
        punkt = 0
        g_o_menu = pygame.font.Font(None, 70)
        g_o_menu_2 = pygame.font.Font(None, 40)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        while done:
            info_string.blit(bg, bg_rect)
            screen.blit(bg, bg_rect)
            screen.blit(g_o_menu.render(u'Игра закончена', 1, (255, 255, 255)), (60, 150))
            screen.blit(g_o_menu_2.render(u'Счёт : ' + str(int(score)), 1, (255, 255, 255)), (180, 210))
            screen.blit(g_o_menu_2.render(u'Лучший счёт: ' + str(int(best_score)), 1, (255, 255, 255)), (125, 250))
            mp = pygame.mouse.get_pos()
            for i in self.punkt_2:
                if mp[0] > i[0] and mp[0] < i[0] + 55 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, g_o_menu_2, punkt)
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    game.menu()
                    done = False
            win.blit(info_string, (0, 0)) 
            win.blit(screen, (0, 30))
            pygame.display.flip()


class GameOver_2:
    def __init__(self, punkt_3 = [120, 140, u'Punkt', (250, 250, 30), (250, 30, 250), 0]):
        self.punkt_3 = punkt_3

    def render(self, a, font, num_punkt):
        for i in self.punkt_3:
            if num_punkt == i[5]:
                a.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                a.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def gameOver(self):
        done = True
        punkt = 0
        g_o_menu = pygame.font.Font(None, 70)
        g_o_menu_2 = pygame.font.Font(None, 30)
        g_o_menu_3 = pygame.font.Font(None, 40)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        while done:
            info_string.blit(bg, bg_rect)
            screen.blit(bg, bg_rect)
            screen.blit(g_o_menu.render(u'Игра закончена', 1, (255, 255, 255)), (60, 150))
            screen.blit(g_o_menu_2.render(u'Повезёт в следующий раз', 1, (255, 255, 255)), (115, 220))
            mp = pygame.mouse.get_pos()
            for i in self.punkt_3:
                if mp[0] > i[0] and mp[0] < i[0] + 55 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, g_o_menu_3, punkt)
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    game.menu()
                    done = False
            win.blit(info_string, (0, 0)) 
            win.blit(screen, (0, 30))
            pygame.display.flip()

            
# Шрифты
pygame.font.init()
hp_font = pygame.font.Font(None, 16) 
# Описание героя 
hero = Player(250, 400)
# Описание целей 
zet = Enemy(250, -60)
zet.right = False
zet_2 = Enemy(250, -120)
zet_2.left = False
zet_3 = Enemy_2(250, -180)
zet_3.right = False
step = 1
# Описание станции
stat = Station(200, 180)
# Описываем снаряды (героя и врагов)
snariad = Weapon(hero.x, hero.y)
snariad.push = False
snariad_2 = Weapon(zet.x, zet.y)
snariad_2.push = False
snariad_3 = Weapon(zet_2.x, zet_2.y)
snariad_3.push = False
snariad_4 = Weapon(zet_3.x - 5, zet_3.y)
snariad_4.push = False
# Режим "Выживание" 
WIDTH = 500
HEIGHT = 500
FPS = 60
# Задаем цвет 
BLACK = (0, 0, 0)
# Создаем игру и окно 
pygame.init()
pygame.mixer.init()
screen_2 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galalga")
clock = pygame.time.Clock()
# Спрайты 
player_img = pygame.image.load('idle_2.png')
meteor_img = pygame.image.load('meteor.png')


class Player_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image = pygame.transform.scale(meteor_img, (40, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


mobs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player_2()
all_sprites.add(player)
for i in range(8):
    mb = Mob()
    all_sprites.add(mb)
    mobs.add(mb) 
# Игровое меню
punkts = [(120, 140, u'Оборона', (255, 255, 255), (250, 250, 30), 0),
          (120, 210, u'Выживание', (255, 255, 255), (250, 250, 30), 1),
          (120, 280, u'Выйти', (255, 255, 255), (250, 250, 30), 2)]
game = Menu(punkts)
game.menu()
# Конец игры (Оборона)
punkt_2 = [(135, 400, u'Главное меню', (255, 255, 255), (250, 250, 30), 0)]
g = GameOver(punkt_2)
# Конец игры (Выживание)
punkt_3 = [(145, 400, u'Главное меню', (255, 255, 255), (250, 250, 30), 0)]
g_2 = GameOver_2(punkt_3)
# Игровой цикл
done = True
pygame.key.set_repeat(1, 1)
pygame.mouse.set_visible(False)
while done:
    if flag == 0:
       # Обработчик событий
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = False
                # Событие - нажатие клавиш 
            if e.type == pygame.KEYDOWN:
                # Перемещение героя 
                if e.key == pygame.K_LEFT:
                    if hero.x > 10:
                        hero.x -= 1
                if e.key == pygame.K_RIGHT:
                    if hero.x < 450:
                        hero.x += 1
                if e.key == pygame.K_UP:
                    if hero.y > 320:
                        hero.y -= 1
                if e.key == pygame.K_DOWN:
                    if hero.y < 400:
                        hero.y += 1
                # Запуск снаряда 
                if e.key == pygame.K_SPACE:
                    if snariad.push == False:
                        snariad.x = hero.x + 15
                        snariad.y = hero.y
                        snariad.push = True
                # Вызов меню
                if e.key == pygame.K_ESCAPE:
                    game.menu()
                    pygame.key.set_repeat(1, 1)
                    pygame.mouse.set_visible(False)
            # Событие - движение мыши 
            if e.type == pygame.MOUSEMOTION:
                m = pygame.mouse.get_pos()
                if m[0] > 10 and m[0] < 450:
                    hero.x = m[0]
                if m[1] > 320 and m[1] < 400:
                    hero.y = m[1]
            # Событие - нажатие кнопок мыши 
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if snariad.push == False:
                        snariad.x = hero.x + 15
                        snariad.y = hero.y
                        snariad.push = True
        # Заливка
        screen.fill((0, 0, 0))
        info_string.fill((50, 50, 50))
        # Передвижение целей        
        if zet.right == True:
            zet.x -= step
            if zet.x < 0:
                zet.right = False
        else:
            zet.x += step
            if zet.x > 450:
                zet.y += move
                zet.right = True
        if zet_2.left == True:
            zet_2.x += step
            if zet_2.x > 450:
                zet_2.left = False
        else:
            zet_2.x -= step
            if zet_2.x < 0:
                zet_2.y += move
                zet_2.left = True
        if zet_3.right == True:
            zet_3.x -= step
            if zet_3.x < 0:
                zet_3.right = False
        else:
            zet_3.x += step
            if zet_3.x > 450:
                zet_3.y += move
                zet_3.right = True
        # Перемещение снаряда
        if snariad.y < 0:
            snariad.push = False
        if snariad.push == False:
            snariad.y = 350
            snariad.x = -10
        else:
            snariad.y -= 3
        # Выстрелы врагов
        if snariad_2.push == False:
            snariad_2.x = zet.x + 15
            snariad_2.y = zet.y
            snariad_2.push = True
        elif snariad_2.y > 500:
            snariad_2.push = False
        if snariad_2.push == False:
            snariad_2.y = zet.y
            snariad_2.x = -10
        else:
            snariad_2.y += scor
        if snariad_3.push == False:
            snariad_3.x = zet_2.x + 15
            snariad_3.y = zet_2.y
            snariad_3.push = True
        elif snariad_3.y > 500:
            snariad_3.push = False
        if snariad_3.push == False:
            snariad_3.y = zet_2.y
            snariad_3.x = -10
        else:
            snariad_3.y += scor
        if snariad_4.push == False:
            snariad_4.x = zet_3.x + 15
            snariad_4.y = zet_3.y
            snariad_4.push = True
        elif snariad_4.y > 500:
            snariad_4.push = False
        if snariad_4.push == False:
            snariad_4.y = zet_3.y
            snariad_4.x = -10
        else:
            snariad_4.y += scor
        # Столкновение снаряда и цели
        if Intersect(snariad.x, zet.x, snariad.y, zet.y, 5, 40) == True:
            snariad.push = False
            zet = Enemy(-60, -60)
            zet.right = False
            step += 0.05
            scor += 0.05
            score += 100
            if move < 50:
                move += 2
        elif Intersect(snariad.x, zet_2.x, snariad.y, zet_2.y, 5, 40) == True:
            snariad.push = False
            zet_2 = Enemy(-60, -60)
            zet_2.left = False
            step += 0.05
            scor += 0.05
            score += 100
            if move < 50:
                move += 2
        elif Intersect(snariad.x, zet_3.x, snariad.y, zet_3.y, 5, 40) == True:
            snariad.push = False
            if en_hp != 0:
                en_hp -= 1
            else:
                en_hp = 1
                if hp < 3:
                    hp += 1
                zet_3 = Enemy_2(-60, -60)
            zet_3.right = False
            step += 0.05
            scor += 0.05
            score += 100
            if move < 50:
                move += 2
        # Столкновение снаряда врага и героя
        if Intersect(snariad_2.x, hero.x, snariad_2.y, hero.y, 5, 40) == True:
            snariad_2.push = False
            hero = Player(250, 400)
            hp -= 1
            if hp == 0:
                hp = 3
                scor = 1
                step = 1
                en_hp = 1
                zet = Enemy(250, -60)
                zet.right = False
                zet_2 = Enemy(250, -120)
                zet_2.left = False
                zet_3 = Enemy_2(250, -180)
                zet_3.right = False
                hero = Player(250, 400)
                g.gameOver()
                score = 0
        elif Intersect(snariad_3.x, hero.x, snariad_3.y, hero.y, 5, 40) == True:
            snariad_3.push = False
            hero = Player(250, 400)
            hp -= 1
            if hp == 0:
                hp = 3
                hp = 3
                scor = 1
                step = 1
                en_hp = 1
                zet = Enemy(250, -60)
                zet.right = False
                zet_2 = Enemy(250, -120)
                zet_2.left = False
                zet_3 = Enemy_2(250, -180)
                zet_3.right = False
                hero = Player(250, 400)
                g.gameOver()
                score = 0
        elif Intersect(snariad_4.x, hero.x, snariad_4.y, hero.y, 5, 40) == True:
            snariad_4.push = False
            hero = Player(250, 400)
            hp -= 1
            if hp == 0:
                hp = 3
                hp = 3
                scor = 1
                step = 1
                en_hp = 1
                zet = Enemy(250, -60)
                zet.right = False
                zet_2 = Enemy(250, -120)
                zet_2.left = False
                zet_3 = Enemy_2(250, -180)
                zet_3.right = False
                hero = Player(250, 400)
                g.gameOver()
                score = 0
        # Столкновение врага и станции 
        if Intersect(zet.x, stat.x, zet.y, stat.y, 5, 40) == True:
            hp = 3
            hp = 3
            scor = 1
            step = 1
            en_hp = 1
            zet = Enemy(250, -60)
            zet.right = False
            zet_2 = Enemy(250, -120)
            zet_2.left = False
            zet_3 = Enemy_2(250, -180)
            zet_3.right = False
            hero = Player(250, 400)
            g.gameOver()
            score = 0
        elif Intersect(zet_2.x, stat.x, zet_2.y, stat.y, 5, 40) == True:
            hp = 3
            hp = 3
            scor = 1
            step = 1
            en_hp = 1
            zet = Enemy(250, -60)
            zet.right = False
            zet_2 = Enemy(250, -120)
            zet_2.left = False
            zet_3 = Enemy_2(250, -180)
            zet_3.right = False
            hero = Player(250, 400)
            g.gameOver()
            score = 0
        elif Intersect(zet_3.x, stat.x, zet_3.y, stat.y, 5, 40) == True:
            hp = 3
            hp = 3
            scor = 1
            step = 1
            en_hp = 1
            zet = Enemy(250, -60)
            zet.right = False
            zet_2 = Enemy(250, -120)
            zet_2.left = False
            zet_3 = Enemy_2(250, -180)
            zet_3.right = False
            hero = Player(250, 400)
            g.gameOver()
            score = 0
        # База данных 
        cur.execute(f'''INSERT INTO Score(score) VALUES({score})''')
        for value in cur.execute(f'''SELECT score from Score ORDER BY score DESC limit 1'''):
            best_score = value[0]
        # Отрисовка объектов
        screen.fill((0, 0, 0))
        screen.blit(bg, bg_rect)
        snariad.render()
        snariad_2.render()
        snariad_3.render()
        snariad_4.render()
        zet.render()
        zet_2.render()
        zet_3.render()
        hero.render()
        stat.render()
        # Отрисовка шрифтов
        info_string.blit(hp_font.render(u'Жизни: ' + str(int(hp)), 1, (0, 0, 0)), (10, 10))
        info_string.blit(hp_font.render(u'Главный корабль: ' + str(int(en_hp) + 1), 1, (0, 0, 0)), (85, 10))
        info_string.blit(hp_font.render(u'Скорость : ' + str(int(step * 100) / 100), 1, (0, 0, 0)), (225, 10))
        info_string.blit(hp_font.render(u'Счёт : ' + str(score), 1, (0, 0, 0)), (325, 10))
        info_string.blit(hp_font.render(u'Лучший счёт : ' + str(best_score), 1, (0, 0, 0)), (390, 10))
        win.blit(info_string, (0, 0))
        win.blit(screen, (0, 30))
        pygame.display.flip()
        pygame.time.delay(5)
    elif flag == 1:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.menu()
                    pygame.key.set_repeat(1, 1)
                    pygame.mouse.set_visible(False)
            if mb.rect.right > player.rect.left and \
                mb.rect.left < player.rect.right and \
                mb.rect.bottom > player.rect.top and \
                mb.rect.top < player.rect.bottom:
                    collide = True
        all_sprites.update()
        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            mobs = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            player = Player_2()
            all_sprites.add(player)
            for i in range(8):
                mb = Mob()
                all_sprites.add(mb)
                mobs.add(mb) 
            g_2.gameOver()
        screen_2.fill(BLACK)
        screen_2.blit(bg, bg_rect)
        all_sprites.draw(screen_2)
        pygame.display.flip()
bd.commit()
cur.close()
    
