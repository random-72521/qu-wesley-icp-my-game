
import pygame as pg
from pygame.sprite import Sprite #Sprite is a base class we can inherit basic attributes and methods from
from settings import *
from utils import *
from os import path

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

        self.spritesheet = SpriteSheet(path.join(self.game.image_dir, "bob_walk_anim1.png")) #provides raster images

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

        self.hit_rect = PLAYER_HIT_RECT

        #states for the player
        self.jumping = False
        self.moving = False
        
        self.last_update = 0
        self.current_frame = 0

        self.coins = 0

        self.load_images()

        print("player instance created")

    def get_keys(self): #gets player input
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        #keybinds, wasd
        if keys[pg.K_w]: 
            self.vel.y = -PLAYER_SPEED

        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED

        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED

        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED

        if self.vel.x != 0 and self.vel.y != 0: #checks if player is moving diagonally
            self.vel *= 0.7071

    def jump(self):
        pass

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]

    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
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
        self.get_keys()

        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

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

        self.animate()


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

        self.load_images()

        print("mob instance created")


    def jump(self):
        pass

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
        self.image.fill(GREEN)

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