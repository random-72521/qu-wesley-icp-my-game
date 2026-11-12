import pygame as pg

WIDTH = 1024
HEIGHT = 768
TILESIZE = 32

#---------Colors---------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 90, 200)
ICE_BLUE = (153, 255, 255)
GREEN = (80, 170, 80)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (85, 85, 85)


#---------Player Settings---------
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE - 5, TILESIZE - 5)
PLAYER_FRIC = -0.1
PLAYER_ACC = 5

#---------Mob Settings---------
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, TILESIZE - 5, TILESIZE - 5)


#---------Game Settings---------
FPS = 120
