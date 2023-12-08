#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, picture, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(
            image.load(picture),
            (width, height)
        )
        self.width = width
        self.height = height
        self.speed = speed
        # создаем физическую модельку спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.width - 5:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 7, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(50, win_width - self.width -   5)
            self.rect.y = -30
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()

img_back = 'galaxy.jpg'
img_rocket = 'rocket.png'
ogg_music = 'space.ogg'
img_enemy = 'ufo.png'
ogg_fire = 'fire.ogg'
img_bullet = 'bullet.png'
img_barrier = 'asteroid.png'

win_width = 700
win_height = 500
display.set_caption('Шутер')
window = display.set_mode((win_width, win_height))
background = transform.scale(
    image.load(img_back),
    (win_width, win_height)
)


mixer.init()
mixer.music.set_volume(0.2)
mixer.music.load(ogg_music)
mixer.music.play()
fire_sound = mixer.Sound(ogg_fire)

font.init()

font_stat = font.SysFont('Arial', 36)
font_end = font.SysFont('Arial', 80)
win = font_end.render('Ты победил!', True, (102, 204, 0))
lose= font_end.render('Ты проиграл!', True, (204, 0, 0))
game = True
finish = False
clock = time.Clock()
FPS = 60
enemy_amount = 5
score = 0
lost = 0
goal = 10
max_lost = 3
lifes = 3
num_fires = 0 
max_fires = 7
reload_time = 3
is_reload = False
barrier_amount = 3

ship = Player(img_rocket, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(enemy_amount):
    monster = Enemy(img_enemy, randint(50, win_width - 85), -40,  80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(barrier_amount):
    asteroid = Enemy(img_barrier, randint(50, win_width - 55), -40,  50, 50, randint(1, 3))
    asteroids.add(asteroid)

bullets = sprite.Group()


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fires < max_fires and is_reload == False:
                    fire_sound.play()
                    ship.fire()
                    num_fires += 1
                if num_fires >= max_fires and is_reload ==  False:
                    last_time = timer()
                    is_reload = True



    if not finish:
        window.blit(background, (0, 0))
        
        
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if is_reload:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font_end.render("Перезарядка...", True, (150, 0, 0))
                window.blit(reload_text, (200, 400))
            else:
                num_fires = 0
                is_reload = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(50, win_width - 85), -40,  80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            lifes -= 1

        if lifes == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        

        text_score = font_stat.render(f'Счёт: {score}',True, (255, 255, 255),)
        window.blit(text_score, (10, 20))
        text_lost = font_stat.render(f'Пропущено: {lost}',True, (255, 255, 255),)
        window.blit(text_lost, (10, 50))

        if lifes == 3:
            life_color = (0, 150, 0)  # зеленый цвет
        # если жизни 2
        elif lifes == 2:
            life_color = (150, 150, 0)  # желтый цвет
        # если жизнь 1
        elif lifes == 1:
            life_color = (150, 0, 0)  # красный цвет

        lifes_text = font_end.render(str(lifes), True, life_color)
        window.blit(lifes_text, (650, 10))
        

    else:
        finish = False
        score = 0
        lost = 0
        num_fires = 0
        lifes = 3
        is_reload = False
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)

        for i in range(enemy_amount):
            monster = Enemy(img_enemy, randint(50, win_width - 85), -40,  80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(barrier_amount):
            asteroid = Enemy(img_barrier, randint(50, win_width - 55), -40,  50, 50, randint(1, 3))
            asteroids.add(asteroid)


        
    display.update()
    clock.tick(FPS)




























