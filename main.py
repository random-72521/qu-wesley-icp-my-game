#File created by Wesley Qu

#I solemnly swear to create concise and informative comments

""" Input
    Process
    Output

    GOALS:
    RULES:
    FEEDBACK:
    FREEDOM:
"""

#import modules
import pygame as pg

#import from py files
from settings import *
from sprites import *

from utils import *

from os import path

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        self.running = True
        self.playing = True

        self.clock = pg.time.Clock() #initializing clock

        self.score = 0
        self.highscore = 0

        print("game instance created")

    def load_data(self, map):
        self.game_dir = path.dirname(__file__) #tell program the the current dir is the dir to use
        self.image_dir = path.join(self.game_dir, "images")
        self.sound_dir = path.join(self.game_dir, "sounds")
        self.map = Map(path.join(self.game_dir, map))
        self.game_save_file = path.join(self.game_dir,"highscore.txt")
        self.pickup_coin_sound = pg.mixer.Sound(path.join(self.sound_dir, "coin_pickup.wav"))

        try:
            with open(self.game_save_file, 'x', encoding="utf-8") as file:
                file.write("Hello, World!")
            print("File created successfully.")
        except FileExistsError:
            print("File already exists. No action taken.")

        # open file and try to set high score with except set high score to zero
        with open(self.game_save_file, 'r') as f:
            try:
                self.highscore = int(f.read())
                print('high score set')
            except:
                self.highscore = 0
                print("high score is zero")


    def new(self):
        self.load_data("level1.txt") #load data from txt file map
        self.all_sprites = pg.sprite.Group() #groups for different sprites
        self.all_walls = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()

        #draws the screen based on .txt file
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1": 
                    Wall(self, col, row) 
                elif tile == "P":
                    self.player = Player(self, col, row) #instantiate player here
                elif tile == "M":
                    self.mob = Mob(self, col, row)
                elif tile == "C":
                    self.coin = Coin(self, col, row)

        #pg.mixer.music.load(path.join(self.sound_dir, "background_music.wav"))
        #pg.mixer.music.play(loops = -1)

    def run(self): #game loop
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 
            self.events() #gets player input
            self.update() #updates the game
            self.draw() #draws sprites

    def events(self): #process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                with open(path.join(self.game_dir, self.game_save_file), 'w') as f:
                    if self.score > self.highscore:
                        f.write(str(self.score))
                    else:
                        f.write(str(self.highscore))
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self): #handles processing of changes based on input
        self.all_sprites.update()

    def draw_text(self, text, size, color, x, y): 
        font_name = pg.font.match_font("arial")
        font = pg.font.Font(font_name, size) #instanantiate Font class

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text(f"FPS: {str(floor(1/self.dt))}", 24, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(f"Coins: {self.player.coins}", 24, WHITE, WIDTH / 2, HEIGHT / 9)
        self.draw_text(f"High Score: {self.highscore}", 24, WHITE, WIDTH / 2, HEIGHT / 12)
        pg.display.flip()


if __name__ == "__main__":
    g = Game()

g.new()

while g.running:
    g.run()

pg.quit()