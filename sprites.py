import pygame as pg
from pygame.sprite import Sprite #Sprite is a base class we can inherit basic attributes and methods from
from settings import *
from utils import *
from os import path

from random import randint

vec = pg.math.Vector2 #initializing vector

def collide_hit_rect(one, two): #returns bool if one is colliding with two
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    if dir == "x": #horizontal collision
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx: 
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2

            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2

            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == "y": #vertical collision
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.width / 2

            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.width / 2

            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(Sprite): #create player class inheriting Sprite with basic attributes and methods
    def __init__(self, game, x, y):
        self.groups = game.all_sprites

        Sprite.__init__(self, self.groups)

        self.game = game

        self.spritesheet = SpriteSheet(path.join(self.game.image_dir, "bob_walk_anim1.png")) #provides raster (pixel) images

        self.up_sprite = SpriteSheet(path.join(self.game.image_dir, "facing_up.png")) 
        self.right_sprite = SpriteSheet(path.join(self.game.image_dir, "facing_right.png")) 
        self.left_sprite = SpriteSheet(path.join(self.game.image_dir, "facing_left.png")) 
        self.down_sprite = SpriteSheet(path.join(self.game.image_dir, "facing_down.png")) 

        self.image = self.right_sprite.get_image(0, 0, TILESIZE, TILESIZE)
        #self.image.set_colorkey(BLACK) #makes all black color on the image transparent

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.vx, self.vy = 0, 0

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        self.hit_rect = PLAYER_HIT_RECT

        #states for the player
        self.dashing = False
        self.moving = False

        self.last = pg.time.get_ticks()
        
        self.last_update = 0
        self.current_frame = 0

        self.cofric = PLAYER_FRIC #coefficient of friction for the player, default is decided by PLAYER_FRIC in settings
        self.coins = 0

        self.load_images()

        self.last_face = "right"

        self.weapon = Weapon(self.game, "hero_sword", "sword", self)

        print("player instance created")

    def get_keys(self): #gets player input
        keys = pg.key.get_pressed()
        #keybinds, wasd
        if keys[pg.K_w]: 
            self.acc.y = -PLAYER_ACC
            self.last_face = "up"
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            self.last_face = "left"
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
            self.last_face = "down"
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
            self.last_face = "right"
        if keys[pg.K_j]:
            if self.weapon.type == "pewpew":
                self.shoot(self.last_face)
            elif self.weapon.type == "sword":
                self.weapon.slash()
        if keys[pg.K_LSHIFT]:
            self.dash()

    def dash(self):
        now = pg.time.get_ticks()
    
        if now - self.last >= PLAYER_DASH_COOLDOWN:
            if self.last_face == "right":
                self.vel += (15, 0)
            elif self.last_face == "up":
                self.vel += (0, -15)
            elif self.last_face == "left":
                self.vel += (-15, 0)
            elif self.last_face == "down":
                self.vel += (0, 15)

        self.last = now



    def shoot(self, direction):
        if direction == "up":
            Projectile(self.game, self.hit_rect.centerx, self.rect.centery, TILESIZE/8, TILESIZE/8, 0, -10)
        if direction == "right":
            Projectile(self.game, self.hit_rect.centerx, self.rect.centery, TILESIZE/8, TILESIZE/8, 10, 0)
        if direction == "down":
            Projectile(self.game, self.hit_rect.centerx, self.rect.centery, TILESIZE/8, TILESIZE/8, 0, 10)
        if direction == "left":
            Projectile(self.game, self.hit_rect.centerx, self.rect.centery, TILESIZE/8, TILESIZE/8, -10, 0)

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]

    def animate(self):
        now = pg.time.get_ticks()
        if not self.dashing and not self.moving:
            if now - self.last_update > 350: #determines when to display next frame, 350ms between each
                self.last_update = now 
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames) 
                #^ creates animation loop
                bottom = self.rect.bottom
                left = self.rect.left
                self.image = self.idle_frames[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left

        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)

                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def update(self): #update player position
        self.animate()
        self.acc = vec(0, 0)
        self.get_keys()

        self.acc += self.vel * self.cofric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #1d kinematic equation for accurately finding new position

        if self.last_face == "up":
            self.image = self.up_sprite.get_image(0, 0, TILESIZE, TILESIZE)


        tile_hits = pg.sprite.spritecollide(self, self.game.all_tiles, False)
        if tile_hits:
            if tile_hits[0].variant == "ice":
                self.cofric = -0.001 #lowers coefficient of friction if player touches ice
            elif tile_hits[0].variant == "mud":
                self.cofric = -0.5
            else:
                self.cofric = -0.1 
        else:
            self.cofric = -0.1
        

        self.rect.center = self.pos

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")

        self.rect.center = self.hit_rect.center

        #checking if the player has collided with a sprite from all_coins
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True) 

        if hits:
            self.coins += 1
            self.game.score += 1
            print(f"{self.coins} coins")
            self.game.pickup_coin_sound.play()
            #for i in range(100):
            #    Particle(self.game, hits[0].rect.x, hits[0].rect.y)


class Mob(Sprite): #class for enemy mobs
    def __init__(self, game, x, y):
        self.groups = game.all_sprites

        Sprite.__init__(self, self.groups)

        self.game = game

        self.spritesheet = SpriteSheet(path.join(self.game.image_dir, "evil_pacman1.png")) #provides raster images

        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)

        self.image.set_colorkey(BLACK) #makes all black color on the image

        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.vx, self.vy = 0, 0

        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        self.hit_rect = MOB_HIT_RECT

        #states for the mob
        self.jumping = False
        self.moving = False
        
        self.last_update = 0
        self.current_frame = 0

        self.hp = 100

        self.load_images()

        print("mob instance created")

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]

    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving: #animation when idle
            if now - self.last_update > 350: #determines when to display next frame, 350ms between each
                self.last_update = now 
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames) 
                #^ creates animation loop
                bottom = self.rect.bottom
                left = self.rect.left
                self.image = self.idle_frames[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.rect.left = left

        elif self.moving: #animation when moving
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)

                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def follow(self, obj):
        direction = vec(obj.rect.centerx - self.rect.centerx, obj.rect.centery - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize()
        self.vel = direction * MOB_SPEED

    def update(self): #update mob position
        self.follow(self.game.player)

        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        hits = pg.sprite.spritecollide(self, self.game.all_projectiles, True) 
        if hits:
            self.hp -= 1

        if self.hp <= 0:
            self.kill()

        hits = pg.sprite.spritecollide(self, self.game.all_weapons, False) 
        if hits:
            self.hp -= 10

        if self.hp <= 0:
            self.kill()

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")

        self.rect.center = self.hit_rect.center

        self.animate()


class Wall(Sprite): 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls

        Sprite.__init__(self, self.groups)

        self.game = game

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_GRAY)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.rect.x = self.x
        self.rect.y = self.y

        print("wall instance created")


class Coin(Sprite): #coin class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins

        Sprite.__init__(self, self.groups)

        self.game = game

        self.image = pg.Surface((TILESIZE, TILESIZE))
        pg.draw.circle(self.image, GOLD, (TILESIZE / 2, TILESIZE / 2), TILESIZE / 2)

        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.rect.x = self.x
        self.rect.y = self.y

        print("coin instance created")

class Particle(Sprite): 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls

        Sprite.__init__(self, self.groups)

        self.game = game

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GOLD)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vel = vec(randint(-180, 180), randint(-180, 180))
        self.pos = vec(x, y)

        self.x = x * TILESIZE 
        self.y = y * TILESIZE 

        self.rect.center = self.pos
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = 15
        self.countdown = Cooldown()
        self.countdown.event_time = floor(pg.time.get_ticks() / 1000)

        print("particle instance created")

    def update(self):
        self.countdown.ticking()
        self.pos += self.vel * self.speed * self.game.dt
        if self.countdown.delta > 1:
            self.kill()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class FloorTile(Sprite):
    def __init__(self, game, x, y, color):
        self.groups = game.all_sprites, game.all_tiles
        Sprite.__init__(self, self.groups)

        self.game = game

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.vel = vec(0,0) 
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos

        self.variant = ""

        print("tile instance created")

class Projectile(Sprite):
    def __init__(self, game, x, y, w, h, sx, sy):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface((w, h))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = TILESIZE / 8
        pg.draw.circle(self.image, GOLD, self.rect.center, self.radius)

        self.rect.x = x
        self.rect.y = y

        self.speed_x = sx
        self.speed_y = sy

        self.fired = False

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.kill()

class Weapon(Sprite):
    def __init__(self, game, sprite, type, player):
        self.groups = game.all_sprites, game.all_weapons
        Sprite.__init__(self, self.groups)

        self.game = game

        self.weapon_image = SpriteSheet(path.join(self.game.image_dir, f"{sprite}.png")) 
        self.image = self.weapon_image.get_image(0, 0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)

        self.type = type

        self.player = player

        self.rect = self.image.get_rect()
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y

        self.attacking = False

    def update(self):
        if self.player.last_face == "right":
            self.rect.x = self.player.rect.x + 32
            self.rect.y = self.player.rect.y
        elif self.player.last_face == "up":
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y - 32
        elif self.player.last_face == "left":
            self.rect.x = self.player.rect.x - 32
            self.rect.y = self.player.rect.y
        elif self.player.last_face == "down":
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y + 32

    def slash(self):
        self.attacking = not self.attacking


