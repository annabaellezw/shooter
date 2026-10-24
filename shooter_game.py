from pygame import *
from random import randint
from time import time as timer

# create window
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

# set title
display.set_caption('Shooter Game')

# background
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

# music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.01)

# player class
class GameSprite(sprite.Sprite):
    # constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # show sprite
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    # movement
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    
lost = 0 #starter value
score = 0

class Enemy(GameSprite):
    # movement
    def update(self):
        #moving down
        self.rect.y += self.speed
        global lost
        #check
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost = lost + 1
            
class Bullet(GameSprite):
    # movement
    def update(self):
        self.rect.y += self.speed
        # klo diatas menghilang
        if self.rect.y < 0:
            self.kill()
            
#create obj
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

#create monsters obj
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

# asteroid
asteroids = sprite.Group()
for i in range(1, 3):
    a = Enemy('asteroid.png', randint(80, win_width-80), -40, 80, 50, randint(1, 7))
    asteroids.add(a)

# sprite group
bullets = sprite.Group()
fire_sound = mixer.Sound('fire.ogg') # sound effect

# for text
font.init()
font2 = font.SysFont('comicsansms', 36)

font1 = font.SysFont('comicsansms', 80)

goal = 10
max_lost = 3

# game loop
run = True
finish = False

rel_time = False # reload
num_fire = 0 # count shots

while run:
    for e in event.get():
        # exit when close button clicked
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN: # press keyboard
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            
    if not finish:
        # show background
        window.blit(background, (0, 0))

        # text
        text_score = font2.render('Score: ' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20)) # show text

        text_missed = font2.render('Missed: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_missed, (10, 50)) # show text

        ship.reset() # show rocket
        ship.update() # movement

        monsters.update() # movement
        monsters.draw(window) # show

        bullets.update() # movement
        bullets.draw(window) # show

        asteroids.update()
        asteroids.draw(window)

                # reload
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (200, 400))
            else:
                # reset
                num_fire = 0
                rel_time = False

        bullet_monster = sprite.groupcollide(monsters, bullets, True, True)
        for b in bullet_monster:
            score = score + 1 # score tambah 1
            monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        bullet_asteroid = sprite.groupcollide(asteroids, bullets, True, True)
        for a in bullet_asteroid:
            score = score + 1 # score bertambah 1
            asteroid = Enemy('asteroid.png', randint(80, win_width-80), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

        if score >= goal:
            finish = True
            win = font1.render('YOU WIN!', True, (255, 255, 255))
            window.blit(win, (200, 200))

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost or sprite.spritecollide(ship, asteroids, False):
            finish = True
            lose = font1.render('YOU LOSE!', True, (255, 0, 0))
            window.blit(lose, (200, 200))

        display.update()
        
        # auto restart
    else: # kalo udah finish
        # reset all variables
        finish = False
        score = 0
        lost = 0
        num_fire = 0

        for b in bullets: # kill bullets
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000) # pause 3s

        # tampilin lagi enemy
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 6):
            asteroid = Enemy('asteroid.png', randint(80, win_width-80), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

    time.delay(50) # 0.05 sec
        
    time.delay(50) # 0.05 sec