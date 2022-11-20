from pygame import *
from random import randint
from time import time as timer
win_width = 700
win_height = 500
w = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
class GameSprite(sprite.Sprite):
    def __init__ (self,player_image,player_x,player_y,size_x,size_y,player_speed,):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        w.blit(self.image, (self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x<625:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 10, 10)
        bullets.add(bullet)
lost = 0
score = 0  
max_lost = 5
max_score = 20
life = 3
oboima = 10
rel_time = False
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
        
        


font.init()
font1 = font.SysFont('Georgia',36)
font2 = font.SysFont('Georgia', 100)
win = font2.render("YOU WIN!!!", True, (255,255,255))
lose = font2.render("YOU LOSE!!!", True, (180,0,0))
text_lose = font1.render("Пропущено:"+ str(lost), True, (255,255,255))
text_score = font1.render("Счёт:"+ str(score), True, (255,255,255))
player = Player('rocket.png', 5, win_height - 100, 80, 100, 10)
enemies = sprite.Group()
bullets = sprite.Group()
for i in range(1, 6):
    enemy = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,2))
    enemies.add(enemy)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroids("asteroid.png", randint(80, win_width - 80), -40, 100, 100, randint(1,2))
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


FPS = time.Clock()
finish = False
game = True
while game == True:
    w.blit(background,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if oboima > 0 and rel_time == False:
                    oboima = oboima - 1
                    player.fire()
                    fire_sound.play()
                if oboima == 0 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                    

            
    if not finish:
        w.blit(background,(0,0))
        player.reset()
        player.update()
        asteroids.draw(w)
        asteroids.update()
        bullets.draw(w)
        bullets.update()
        enemies.draw(w)
        enemies.update()
        display.update()

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                text_reload = font1.render("ПЕРЕЗАРЯДКА", 1,(255,0,0))
                w.blit(text_reload,(260,460))
            else:
                oboima = 10
                rel_time = False

        collides = sprite.groupcollide(enemies,bullets, True, True)
        for i in collides:
            score += 1 
            enemy = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,2))
            enemies.add(enemy)

        if sprite.spritecollide(player, asteroids, True):
            asteroid = Asteroids("asteroid.png", randint(80, win_width - 80), -40, 100, 100, randint(1,2))
            asteroids.add(asteroid)
            life -= 1
            
        if lost >= max_lost or life == 0:
            finish = True
            w.blit(lose,(200,200))
        if score >= max_score:
            finish = True
            w.blit(win,(200,200))
        text_lose = font1.render("Пропущено:"+ str(lost), True, (255,255,255))
        w.blit(text_lose,(10,50))
        text_score = font1.render("Счёт:"+ str(score), True, (255,255,255))
        w.blit(text_score,(10,30))
        text_life = font1.render("Здоровье:"+ str(life), True, (255,255,255))
        w.blit(text_life,(10,10))
        display.update()
        FPS.tick(60)