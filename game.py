# This file contains the Game class
# where the game is played while in a level or playing multiplayer
# controlled by "main.py" file

from Menu import *


class Game:
    def __init__(self):
        # called when g object is created in file "main.py"
        # To initialise game screen, type of game, pygame and game variables

        # pygame screen initialization
        pg.init()
        pg.mixer.init()
        self.m = Menu(self)
        self.screen = pg.display.set_mode((screen_width, screen_height))

        #self.game_font = pg.font.match_font(game_font)
        self.game_font = "/System/Library/Fonts/Supplemental/Arial.ttf"
        self.clock = pg.time.Clock()
        pg.display.set_caption(Title)
        self.is_playing = None

        # basic game variables
        self.alarm_is_playing = False
        self.running = True
        self.next_action = False
        self.player_n = 1   # set default to 1
        self.number_of_players = 0  # set default to 0
        self.level = 0
        self.image = None
        self.multiplayer=False
        self.game_status = None
        self.volume = game_volume
        self.knife_image = knifesdict["3"]
        self.filter = None
        self.FPS = FPS
        self.is_connected_to_server = False
        self.selected_player = 1
        self.score = 0
        self.opp_score = 0

        # keys
        self.left_key = left_key
        self.right_key = right_key
        self.jump_key = jump_key


    # primary functions  /  Game LOOP
    def new(self):
        # called when starting a new game

        if not self.running:
            return

        # sound management
        if self.alarm_is_playing:
            self.is_playing = None
            pg.mixer.stop()
        if self.is_playing != 'game':
            self.sound_management("game")

        # create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.knifes = pg.sprite.Group()
        self.opp_knifes = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.knifes_for_counter = pg.sprite.Group()
        self.health_hearts = pg.sprite.Group()
        self.guards = pg.sprite.Group()
        self.supplements = pg.sprite.Group()

        # game variables
        self.old_n_knifes = 0
        self.old_n_lives = 0
        self.level_ended = False
        self.level2guards_spawned = False
        self.level4guards_appear = False
        self.last_update = 0
        self.pause = None
        self.game_status = None
        self.alarm_is_playing = False
        self.previous_data = [[0, 0], [0, 0], 0, [0, 0], 0, [0, 0], 0]
        self.opponent_knives_list = [0, Ennemy_Knife, 0, Ennemy_Knife, 0, Ennemy_Knife]
        self.n_of_dead_guards = 0
        self.all_guards_are_dead = False
        self.colliding_platforms = []


        self.create_map()
        if self.multiplayer:    # to send first player position to server and get opponent position
            print("Player number : ", self.player_n)
            self.n.send(self.encode(self.player.pos))
            self.p2 = Opponent_multi(self, 0, 0)


        self.run()

    def run(self):
        # game loop
        # Where the game runs while playing a level

        self.game_start_time = pg.time.get_ticks()
        self.playing = True
        while self.playing:
            self.clock.tick(self.FPS)
            self.events()
            if not self.playing:
                return
            self.update()
            self.draw_backround()
            self.specific_level_actions()
            self.draw_sprites()

    def update(self):
        # function of main game loop, updates all the different sprites and platforms colliding with player
        self.all_sprites.update()
        self.supplements.update()
        self.colliding_platforms.clear()
        self.platforms.update()

    def events(self):
        # game loop - events
        # function of the main game loop
        # this function is used to check for events
        # this function only quits game and loops when user wants to quit or level is finished
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

        if self.multiplayer:
            if self.p2.is_dead:
                self.score += 1
                self.m.End_screen(self.screen, self.level, True)
                for sprites in self.all_sprites:
                    sprites.kill()
                self.playing = False

        if len(self.guards) == self.n_of_dead_guards:
            self.all_guards_are_dead = True

        if self.level_ended:
            self.filter = None
            self.m.End_screen(self.screen, self.level, True)
            for sprites in self.all_sprites:
                sprites.kill()
            self.playing = False

        if self.player.is_dead:
            if self.multiplayer:
                self.opp_score += 1
            self.m.End_screen(self.screen, self.level, False)
            for sprites in self.all_sprites:
                sprites.kill()
            self.playing = False

    def draw_backround(self):
        # this function draws the backround depending on the level
        if self.image:
            self.screen.blit(self.image, (0,0))
        else:
            self.screen.fill(bg_color)

    def draw_sprites(self):
        # function of the main game loop
        # draws all the updated sprites on screen
        #self.draw_grid()

        # draw all sprites and counters on screen
        self.all_sprites.draw(self.screen)
        self.draw_info()

        if self.filter:
            self.screen.blit(self.filter, (0, 0))

        # pause button
        if self.m.img_button(self.screen, pause_button.convert_alpha(), 10, 10, (50, 50), (70, 70), rotate=0):
            self.m.Pause(self.screen)
        pg.display.flip()

    # MENU
    def menu(self):
        # This is where we use the menu class to browse between menu screens and gamemodes
        self.menu_running = True

        # sound
        if self.next_action != "PLAYGAME":
            self.sound_management("menu")

        # sets next action to go to start screen if the menu is openned for the first time
        if not self.next_action:
            self.next_action = "Start"

        while self.menu_running:
            if self.next_action == "Start":
                self.m.Start_screen(self.screen)
            if self.next_action == "campaign":
                self.m.Campaign(self.screen)
            if self.next_action == "PLAYGAME":
                return
            if self.next_action == "multiplayer":
                self.m.Multiplayer(self.screen)
            if self.next_action == "Highscores":
                self.m.Highscores(self.screen)
            if self.next_action == "Settings":
                self.m.Settings(self.screen)
            time.sleep(0.3)
            if self.next_action == "QUIT":
                self.running = False
                self.menu_running = False

    # secondary
    def specific_level_actions(self):
        # where and when the level ends
        # draws commentaries and update map backrounds depending on the level
        if self.level == 1:
            self.draw_text("You have just broken the back wall of your cell", 25, white, 370, 150)
            self.draw_text("Try and exit through the sewer", 25, white, 370, 200)
            self.player.knife_counter=0
            if self.player.pos.x < 0:
                self.player.health = 0
                self.level_ended = True
        if self.level == 2:
            if self.player.pos.x < 0:
                self.level_ended = True
            if self.game_status == None:
                self.player.knife_counter=0
            if self.cam.alarm:
                # if the alarm saw the player
                if not self.alarm_is_playing:
                    self.sound_management("alarm")
                # to manage the laser and red alarm for level 2
                self.draw_text("Uh oh, the guards are here ! ", 25, red, 450, 350)
                self.draw_text("Kill them and exit the level", 25, red, 450, 400)
                self.spawn_guards_level2()
                now = pg.time.get_ticks()
                if now - self.last_update > 300:
                    self.filter = self.level2_alarm_backround[1]
                    if now - self.last_update > 600:
                        self.filter = None
                        self.last_update = now
            else:
                # draw laser line and cache
                pg.draw.line(self.screen, red, self.cam.fov_pos,
                             self.cam.fov_pos + self.cam.direction.rotate(self.cam.angle), 3)
                self.screen.blit(self.level2_cache, (0, 0))

            # commentaries
            if self.game_status == None:
                self.draw_text("Get to the upper left cell to get knives", 25, white, 450, 30)
            if self.game_status == "openned":
                self.draw_text("Well done, now try and exit without alerting the guards", 25, white, 500, 30)
        if self.level == 3:
            if self.player.pos.x < 0:
                self.level_ended = True
        if self.level == 4:
            # for left hidden part and flashing light
            if self.player.pos[0] < 570 and self.player.pos[1] > 480 and not self.game_status:
                self.game_status = "normalview"
                self.image = self.level4_light[0]
            if self.game_status == "normalview":
                now = pg.time.get_ticks()
                if (now - self.last_update) > 700:
                    if random.randint(0, 1) == 0:
                        self.image = self.level4_light[(self.current_frame+1)%2]
                        self.last_update = now
                        self.current_frame += 1
                if not self.level4guards_appear:
                    for guard in self.guards:
                        self.all_sprites.add(guard)

            if self.player.pos.x < 0:
                self.level_ended = True
        if self.level == 5:
            if self.game_status == "got_the_key":
                # draw key next to knifes
                if 400<self.player.pos.y<470 and 570<self.player.pos.x<660:
                    self.game_status = "unlocked"
                    for plat in self.door_plats:
                        plat.kill()
            if self.game_status == "unlocked":
                self.image = self.level5_unlocked_image
            if self.player.pos.x < 0:
                self.level_ended = True

        if self.multiplayer:
            self.server_communication()

    def server_communication(self):
        # This function is used to communicate with the server when playing multiplayer
        send = self.encode(self.player.pos) # encode player data
        reply = self.n.send(send)      # send player data to opponent
        if reply and reply != "connected":
            if reply == "0000":
                self.p2.is_dead = True
                self.p2.kill()
            else:
                data = self.decode(reply)
                self.p2.pos = data[0]
                i=1         #update pos opponent
                while i < 7:
                        if self.previous_data[i][0] == 0 and data[i][0] != 0:
                            # create knife sprite if it was not there before
                            k = Ennemy_Knife(self, data[i], data[i+1])
                            self.opponent_knives_list[i] = k    # add knive in knife list
                        elif self.previous_data[i][0] != 0 and data[i][0] == 0:
                            # kill knife sprite if it is not there and was there before
                            self.opponent_knives_list[i].kill()
                        else:
                            # update position and angle of existing knife
                            self.opponent_knives_list[i].pos = data[i]
                            self.opponent_knives_list[i].angle = data[i+1]
                        i += 2
                self.previous_data = data

    def connect_to_server(self):
        # function called once when starting a new multiplayer game
        # connects to server by creating n object for class Network
        self.n = Network()

    def draw_info(self):
        # called in draw function of the main loop
        # draw knife counter
        for i in range(self.player.knife_counter):
            image = pg.transform.rotate(pg.transform.scale(self.knife_image.convert().convert_alpha(), (70, 30)), -90)
            self.screen.blit(image, (screen_width - 200 - i * 30, 10))

        # draw life counter
        for i in range(self.player.health):
            image = pg.transform.scale(life_image.convert().convert_alpha(), (30, 30))
            self.screen.blit(image, (screen_width - 70 - i * 40, 10))

        # opponent draw_life
        if self.multiplayer:
            self.p2.draw_life()


    def draw_text(self, text, size, color, x, y):
        # to draw any text on the screen
        # x, y correspond to coordinates of the middle top of textbox
        font = pg.font.Font(self.game_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def create_map(self):
        # function called when lanching a new game, sets player animation folder,
        # reads from mapfile
        # creates sprites

        # find correct player animation folder
        if self.level != 0:
            self.multiplayer = False
            self.player_folder = player_folders[3][1]
        else:
            self.player_folder = player_folders[self.selected_player][1]

        # make the map data into a list
        self.load_backround_images()
        mapfile = levelmapsdict[str(self.level)]
        self.map_data = []

        # create a list containing the positions of plats, players and sprites
        file = open(os.path.join(map_folder, mapfile), "r")
        for line in file:
            self.map_data.append(line.strip())

        # check for correct size
        # prints: "Map Size Error" if map file is of incorrect size
        if len(self.map_data) == 20:
            for i in range(20):
                if len(self.map_data[i]) != 30:
                    print("Map Size Error")
        else:
            print("Map Size Error")

        # create sprites depending on their positions
        y = 0
        for row in self.map_data:
            i=0
            while i < len(row):
                if row[i] == "-" or row[i] == "i" or row[i] == "a":
                    Platform(self, i, y, row[i])
                if row[i] == str(self.player_n):
                    self.player = Player(self, i * TILESIZE, y * TILESIZE)
                if row[i] == 'C':
                    Cell(self, i, y)
                if row[i] == 'g':
                    Guard(self, i, y)
                if row[i] == 'G':
                    Guard(self, i, y, status='idle')
                if row[i] == 'c':
                    self.cam = Camera(self, i, y)
                if row[i] == 'k':
                    Knife_box(self, i, y)
                if row[i] == 'l':
                    Life_bonus(self, i, y)
                if row[i] == 'K':
                    Key(self, i, y)
                i += 1
            y += 1
        time.sleep(1)

    def draw_grid(self):
        # this function draws grid on screen (square tiles)
        # used for devellopong purposes
        for x in range(0, screen_width, TILESIZE):
            pg.draw.line(self.screen, light_blue, (x, 0), (x, screen_height))
        for y in range(0, screen_height, TILESIZE):
            pg.draw.line(self.screen, light_blue, (0, y), (screen_width, y))

    def decode(self, data):
        # decodes data recieved from the server and puts it in a list
        self.p2.health = int(data[-1:])
        data = data[:-2]
        data = data.split(";")
        knifes = False
        output = []
        playerpos = data[0].split(",")
        for i in range(2):
            playerpos[i] = float(playerpos[i])
        output.append(playerpos)
        if len(data)>1:
            knifes = True
        if knifes:
            for i in range(len(data)-1):
                i+=1
                knifepos = data[i].split(',')[:-1]
                knifeangle = float(data[i].split(',')[-1:][0])
                for i in range(2):
                    knifepos[i] = float(knifepos[i])
                output.append(knifepos)
                output.append(knifeangle)
        return output

    def encode(self, player_pos):
        # encodes data to send to server as a string
        output = str(round(player_pos[0], 3)) + "," + str(round(player_pos[1], 3))
        for knife in self.knifes:
            output += ";" + self.encode_knife(knife.pos, knife.image_rotation_angle)
        i = len(self.knifes)
        for knife in range(3-i):
            output += ";0,0,0"
        output += "h" + str(self.player.health)
        return output

    def encode_knife(self, knifepos, knifeangle):
        # called by encode, encodes knife positions and angles as string
         return str(round(knifepos[0], 2)) + "," + str(round(knifepos[1], 2)) + "," + str(round(knifeangle, 2))

    def spawn_guards_level2(self):
        # spawns guard level 2 when player hits laser
        if not self.level2guards_spawned:
            Guard(self, 26, 4)
            Guard(self, 2, 11)
            self.level2guards_spawned = True

    def sound_management(self, state):
        # this function manages sound in the game,
        # plays sound corresponding to argument "state"
        if state == "menu":
            pg.mixer.stop()
            buffer = pg.mixer.Sound(os.path.join(sound_folder, sounds_dict["menu_music"]))
            buffer.set_volume((self.volume) / 100)
            pg.mixer.Sound.play(buffer, -1, fade_ms=2000)
            self.is_playing = state
        if state == "game":
            if self.is_playing != 'game':
                pg.mixer.stop()
            buffer = pg.mixer.Sound(os.path.join(sound_folder, sounds_dict["game_music"]))
            buffer.set_volume((self.volume)/100)
            pg.mixer.Sound.play(buffer, -1, fade_ms=2000)
            self.is_playing = state
        if state == "button_click":
            pg.mixer.Sound.play(pg.mixer.Sound(os.path.join(sound_folder, sounds_dict["button_click"])))
        if state == "knife_throw":
            buffer = pg.mixer.Sound(os.path.join(sound_folder, sounds_dict["knife_throw"]))
            buffer.set_volume(self.volume/100)
            pg.mixer.Sound.play(buffer)
        if state == "hit":
            buffer = pg.mixer.Sound(os.path.join(sound_folder, sounds_dict["hit"]))
            buffer.set_volume(self.volume/ 100)
            pg.mixer.Sound.play(buffer)
        if state =="land_on_plat":
            sound = pg.mixer.Sound(os.path.join(sound_folder, sounds_dict["land_on_plat"]))
            sound.set_volume(self.volume / 100)
            pg.mixer.Sound.play(sound)
        if state == "alarm":
            sound = pg.mixer.Sound(os.path.join(sound_folder, sounds_dict["alarm"]))
            sound.set_volume(0.2*(self.volume) / 100)
            pg.mixer.Sound.play(sound, -1)
            self.alarm_is_playing = True
        if state == "jump":
            sound = pg.mixer.Sound(os.path.join(sound_folder, sounds_dict["jump"]))
            sound.set_volume(self.volume / 100)
            pg.mixer.Sound.play(sound)

    def load_backround_images(self):
        # loads backround images when there are multiples ones
        # made for efficiency
        # to avoid loading each image at each iteration of main loop
        # only called once
        self.image = pg.image.load(levelbakcroundict[str(self.level)]).convert()
        if self.level == 2:
            self.level2_cache = pg.image.load(level_2_supplements["laser_cache"]).convert().convert_alpha()
            red  = pg.image.load(red_filter).convert()
            red.set_alpha(200)
            self.level2_alarm_backround = [self.image, red]
            self.current_frame = 0
        if self.level == 4:
            self.level4_light = [self.image, pg.image.load(level_4_supplements["light_on"]).convert()]
            self.image = self.level4_left_part_hidden = pg.image.load(level_4_supplements["only_right"])
            self.current_frame = 0
        if self.level == 5:
            self.level5_unlocked_image = pg.image.load(level_5_supplements["unlocked"])
            self.current_frame = 0
            self.door_plats = [Platform(self, 19, 14, "-"), Platform(self, 20, 14, "-")]

