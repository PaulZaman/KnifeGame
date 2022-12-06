#Settings

import os
import pygame as pg
import random
import math
vec = pg.math.Vector2

# screen parameters
Title = "Knife escape"
screen_width = 900
screen_height = 600
FPS = 70
TILESIZE = 30
GRIDWIDTH = screen_width / TILESIZE
GRIDHEIGHT = screen_height / TILESIZE
game_font = "arial"
game_volume = 100

#player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 0.5
JUMP_HEIGHT = -10
NUMBER_OF_KNIFES = 3
PLAYER_HEALTH = 3
GUARD_SPEED = 1
GUARD_HEALTH = 3

#knifes
KNIFE_RATE = 150
KNIFE_GRAV = 0.2
KNIFE_SPEED = 10

#colors
sky_blue = (0,128,255)
black = (0,0,0)
bg_color = black
red = (255,0,0)
grey = (30,30,30)
blue = (0,0,255)
light_blue = (100, 100, 255)
white = (255, 255, 255)
darkmagenta = (139,0,139)
light_grey = (100, 100, 100)
dark_grey = (20, 20, 20)
less_white = (160, 160, 160)
green = (0, 255, 0)

#           commands for platforms collisions  (for making maps)
#   - = only up
#   i = up and sides
#   a = all four sides


# Set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "png")
map_folder = os.path.join(game_folder, "Maps")
map_backround_folder = os.path.join(map_folder, "backrounds")
menu_folder = os.path.join(os.path.join(game_folder, "Menu"))
menu_bg_folder = os.path.join(menu_folder, "Menu_bg")
menu_buttons_folder = os.path.join(menu_folder, "Menubuttons")
Main_menubg = pg.image.load(os.path.join(menu_bg_folder, "menu_bgd.jpg"))
celldoor_folder = os.path.join(img_folder, "cell")
progress_file = os.path.join(game_folder, 'progress.txt')
highscores_file = os.path.join(game_folder, 'Highscores.txt')
sound_folder = os.path.join(game_folder, 'Sounds')
player_animation_folder = os.path.join(img_folder, "players")
knifes_folder = os.path.join(img_folder, "knifes")
guard_animation_folder = os.path.join(img_folder, "guard")



# players folders
cowboy_folder = os.path.join(player_animation_folder, "cowboy")
ninja_folder = os.path.join(player_animation_folder, "ninja")
ninja_girl_folder = os.path.join(player_animation_folder, "ninja_girl")
prisonner_folder = os.path.join(player_animation_folder, "prisonner")
player_folders = [("The Cowboy", cowboy_folder), ("The Ninja", ninja_folder), ("The girl Ninga", ninja_girl_folder), ("The escape", prisonner_folder)]

# knife images / folders
knifesdict = {"1":"knife1.png", "2":"knife2.png", "3":"knife3.png", "4":"knife4.png"}
for knife in knifesdict:
    knifesdict[str(knife)] = pg.image.load(os.path.join(knifes_folder,  knifesdict[str(knife)]))


# LEVELS, sprites AND SOUND
pause_button = pg.image.load(os.path.join(menu_buttons_folder, "pause_button.png"))
levelmapsdict = { "0":"Multiplayer.txt", "1":"Map1.txt", "2":"Map2.txt", "3": "Map3.txt", "4":"Map4.txt", "5":"Map5.txt"}
levelbakcroundict = {"0":"multi.png", "1":"level1.jpg", "2":"Level2.jpg", "3":"Level3.jpg", "4":"Level4.jpg", "5":"level5.jpg"}
for map in levelbakcroundict:
    levelbakcroundict[str(map)] = os.path.join(map_backround_folder, levelbakcroundict[str(map)])
level_4_supplements = {"only_right" : os.path.join(map_backround_folder, "level4_right.jpg"), "light_on": os.path.join(map_backround_folder, "level4_light.jpg")}
level_2_supplements = {"red" : os.path.join(map_backround_folder, "level2-red.jpg"), "laser_cache": os.path.join(map_backround_folder, "level2-bis.jpg")}
level_5_supplements = {"unlocked": os.path.join(map_backround_folder, "level5_unlocked.jpg")}

life_image = pg.image.load(os.path.join(img_folder, "heart.png"))
key_image = pg.image.load(os.path.join(img_folder, "key.png"))

knife_box_image = pg.image.load(os.path.join(img_folder, "knife_box.jpg"))
red_filter = os.path.join(img_folder, "FILTRE_ROUGE1.png")
celldict = {"1": "1.jpg", "2": "2.jpg", "3": "3.jpg", "4": "4.jpg", "5": "5.jpg", "6": "6.jpg", "7": "7.jpg", "8": "8.jpg", "9": "9.jpg", "10": "10.jpg", "11": "11.jpg", "12": "12.jpg", "13": "13.jpg"}
sounds_dict = {"alarm": "alarme.ogg", "jump": "souffle.ogg", "land_on_plat":"land_on_plat.ogg", "knife_throw": "knife_throw.ogg", "hit":"hit.ogg", "menu_music":"menu_music.ogg", "button_click":"button_click.ogg", "game_music": "game_music.ogg"}


# keys for movement and jumping

left_key = pg.K_q
right_key = pg.K_d
jump_key = pg.K_z
