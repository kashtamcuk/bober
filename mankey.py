from pygame import*
from random import randint




font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render("YOU LOSe!", True, (180, 0, 0))


img_bullet = "snarad.PNG"
img_enemy = "gorila.PNG"

score = 0
lost = 0
max_lost = 3
goal = 1

clock = time.Clock()
FPS = 15
width = 600
height = 700

window = display.set_mode((width, height))
display.set_caption('Мафія')

background = transform.scale(image.load("gungles.png"),(600, 700))



walk_left = [
    image.load("left1.png"),
    image.load("left2.png"),
    image.load("left3.png")
]

walk_right = [
    image.load("right1.png"),
    image.load("right2.png"),
    image.load("right3.png")
]





class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_y, player_x, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.left = False
        self.right = False
        self.count = 0
    def Mankey(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Mankey(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.left = True
            self.right = False
        elif keys[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False
            self.count = 0
    def animation(self):
        if self.count + 1 >= 15:
            self.count = 0
        if self.left == True:
            window.blit(walk_left[self.count // 5], (self.rect.x, self.rect.y))
            self.count += 1
        elif self.right == True:
            window.blit(walk_right[self.count // 5], (self.rect.x, self.rect.y))
            self.count += 1
        else:
            window.blit(self.image, (self.rect.x,self.rect.y))
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 40, 40, -15)   
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("gorila.PNG", randint(
        80, width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
    
            
        
mankey = Mankey("wpered.png",500,490,70,70,4)

mixer.init()
mixer.music.load('fom myisik.mp3')
mixer.music.play(-1)
mixer.music.set_volume(1)
fire_sound = mixer.Sound('kndok.mp3')
finish = False

game = True
while game:

    window.blit(background,(0, 0))

   
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                mankey.fire()
            
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
            
        mankey.update()
        monster.update()
        bullets.update()

        mankey.animation()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Mankey(img_enemy, randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(monster, monster, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        display.update()
    clock.tick(FPS)
