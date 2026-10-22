import pygame as pg

WIDTH = 1024
HEIGHT = 768
TILESIZE = 32

#---------Colors---------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 90, 200)
GREEN = (80, 170, 80)
GOLD = (255, 215, 0)


#---------Player Settings---------
PLAYER_SPEED = 200
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE - 5, TILESIZE - 5)

#---------Mob Settings---------
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, TILESIZE - 5, TILESIZE - 5)


#---------Game Settings---------
FPS = 60
