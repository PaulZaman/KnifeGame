from sprites import *
import time
from network import Network

class Menu():
    def __init__(self, game):
        self.clock = pg.time.Clock()
        self.game = game
        self.selected_player = 1
        self.opponent_player = 1

    def Start_screen(self, screen):
        #   Start screen, returns what next action is to be executed
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        screen.blit(self.image, (0, 0))
        run = True
        while run:
            if self.button(screen, "Campaign", black, white, 1*GRIDWIDTH/4, 13, 10, 2):
                self.game.next_action="campaign"
                return
            if self.button(screen, "Multiplayer", black, white, 3*GRIDWIDTH/4, 13, 10, 2):
                self.game.next_action = "multiplayer"
                return
            if self.button(screen, "Highscores", black, white, 3 * GRIDWIDTH / 4, 16, 10, 2):
                self.game.next_action = "Highscores"
                return
            if self.button(screen, "Settings", black, white, 1 * GRIDWIDTH / 4, 16, 10, 2):
                self.game.next_action = "Settings"
                return
            if self.button(screen, "EXIT", black, white, GRIDWIDTH/2, GRIDHEIGHT-1.5, 10, 1.5):
                self.game.next_action="QUIT"
                return
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.next_action = "QUIT"
                    self.game.menu_running = False
                    return

    def Campaign(self, screen):
        # This us the campaign screen in the menu
        time.sleep(0.3)
        unlock_all = False
        cross_image = pg.transform.scale(pg.image.load(os.path.join(img_folder, 'kroi.png')), (300, 60))
        before_unlock_all = False
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        run = True
        while run:
            screen.blit(self.image, (0, 0))
            level_y = 6
            self.get_progress()
            self.draw_text(screen, "You have to escape the prison", 30, white, GRIDWIDTH/2, 4)
            for i in range(1, 6):
                if self.button(screen, "Level" + str(i), blue, white, GRIDWIDTH/2, level_y, 10, 2) and self.levels_status[str(i)] == 'unlocked':
                    self.game.level = i
                    self.game.next_action = "PLAYGAME"
                    return
                if self.levels_status[str(i)] == 'locked':
                    screen.blit(cross_image, (TILESIZE*(-5+GRIDWIDTH/2), TILESIZE*(level_y)))
                    self.draw_text(screen, "locked", 30, red, 7 + GRIDWIDTH / 2, level_y)
                level_y += 2.3
                i += 1
            self.draw_text(screen, "Unlock all levels : ", 25, white, 4, 11)
            unlock_all = self.switch(screen, 4, 12, 4, 2, unlock_all, light_grey)
            if unlock_all:
                for i in range(1, 6):
                    self.update_progress(i, "unlocked")
            elif unlock_all != before_unlock_all and not unlock_all:
                for i in range(2, 6):
                    self.update_progress(i, "locked")
            before_unlock_all = unlock_all
            if self.return_to_menu(screen):
                self.game.next_action = "Start"
                return

            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.next_action = "QUIT"
                    self.game.menu_running = False
                    return

    def Highscores(self, screen):
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        screen.blit(self.image, (0, 0))
        self.get_highscores()
        self.draw_highscores(screen, 100, 170, screen_width - 200, screen_height - 250)

        run = True
        while run:


            if self.return_to_menu(screen):
                self.game.next_action = "Start"
                return
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.next_action = "QUIT"
                    self.game.menu_running = False
                    return

    def Multiplayer(self, screen):
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        self.game.connect_to_server()
        player_n = self.game.n.get_player_number()
        self.ready_or_not = "not_ready"
        self.before_ready_or_not = "not ready"
        if player_n:
            image = pg.image.load(os.path.join(player_folders[self.selected_player][1], "Idle__000.png")).convert().convert_alpha()
            red_coeff = find_reduction_coefficient(image, 250)
            image = pg.transform.scale(image, (int(image.get_width() * red_coeff), int(image.get_height() * red_coeff)))
            image = image.convert_alpha()
        run = True
        while run:
            screen.blit(self.image, (0, 0))
            if player_n:
                self.draw_text(screen, "Connected", 40, green, GRIDWIDTH/2, -5+GRIDHEIGHT / 2)
                self.draw_text(screen, "Player number: ", 40, white, GRIDWIDTH/2, (GRIDHEIGHT / 2)-1 )
                self.draw_text(screen, player_n, 40, white, GRIDWIDTH/2, (GRIDHEIGHT / 2))
                self.draw_text(screen, "YOU:", 40, white, 4, 3)

                self.ready_not_ready_button(screen, self.ready_or_not, GRIDWIDTH/2, 16, 6, 1.5)

                screen.blit(image, (120-image.get_width()/2, 420-image.get_height()))   # draw selected_player

                if self.button(screen, "Change caracter", white, black, 4, 15, 7.5, 2):
                    self.ready_or_not = "not_ready"
                    new_player = self.Choose_player(screen)
                    if new_player == "QUIT":
                        self.game.next_action = "QUIT"
                        self.game.menu_running = False
                        return
                    if new_player != self.selected_player:
                        self.selected_player = new_player
                        image = pg.image.load(
                            os.path.join(player_folders[self.selected_player][1], "Idle__000.png")).convert()
                        red_coeff = find_reduction_coefficient(image, 300)
                        image = pg.transform.scale(image, (int(image.get_width() * red_coeff), int(image.get_height() * red_coeff)))
                        image =image.convert_alpha()

                if self.ready_or_not == "ready":    # if player is ready to play
                    opponent_player = self.game.n.check_if_opponent_is_ready(self.selected_player)
                    if opponent_player:
                        pg.display.flip()
                        self.game.opponent_player = int(opponent_player)
                        self.game.selected_player = self.selected_player
                        self.game.player_n = player_n
                        self.game.number_of_players = 2
                        self.game.multiplayer = True
                        self.game.level = 0
                        self.game.next_action = "PLAYGAME"
                        time.sleep(0.2)
                        return
                if self.ready_or_not == "not_ready" and self.before_ready_or_not == "ready":
                    self.game.n.send("not_ready")

            else:
                self.draw_text(screen, "Not connecting to server", 40, red, GRIDWIDTH / 2, GRIDHEIGHT / 2)
                if self.button(self.game.screen, "Try again ?", blue, white, 20, 22, 1, 10):
                    self.game.next_action = "multiplayer"
                    return

            if self.return_to_menu(screen):
                self.game.next_action = "Start"
                return
            pg.display.flip()
            self.clock.tick(20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.next_action = "QUIT"
                    self.game.menu_running = False
                    return
            self.before_ready_or_not = self.ready_or_not

    def End_screen(self, screen, level, finish):
        # this screen is for when the game ends
        self.time_is_saved = False
        highscore = False
        asked_for_rematch = False
        self.rematch_denied = False
        self.image =  self.game.image
        self.get_highscores()
        if finish and not self.game.multiplayer:
            # get level time, update progress(unlock next level)
            now = pg.time.get_ticks()
            finish_time = (now-self.game.game_start_time)/1000
            self.update_progress(level+1, "unlocked")
            # figures out if player score a high score
            if self.highscores[str(level)][1] == 'None':
                highscore = True
            elif finish_time < float(self.highscores[str(level)][1]):
                highscore = True

            name = ""
        run = True
        while run:
            screen.blit(self.image, (0, 0))
            self.game.all_sprites.draw(screen)

            # If player finished level and is not playing multiplayer
            if finish and not self.game.multiplayer:
                self.finished(highscore, screen, level, finish_time, name, now)
                if self.button(screen, "Play again", black, blue, GRIDWIDTH / 2, -2 + GRIDHEIGHT / 2, 6, 2):
                    self.game.level = level
                    self.game.next_action = "PLAYGAME"
                    self.game.player.kill()
                    return
                if self.button(screen, "Next Level", black, blue, GRIDWIDTH / 2, 1 + GRIDHEIGHT / 2, 6, 2):
                    self.game.level = level + 1
                    self.game.next_action = "PLAYGAME"
                    self.game.player.kill()
                    return

            # if player won and is playing multiplayer
            elif self.game.multiplayer:
                if finish:
                    self.draw_text(screen, "Well done !", 50, blue, GRIDWIDTH / 2, -5 + GRIDHEIGHT / 2)
                else:
                    self.draw_text(screen, "You Died !", 50, red, GRIDWIDTH / 2, -5 + GRIDHEIGHT / 2)

                # draw score
                self.draw_text(screen, "Score : ", 30, white, -5+GRIDWIDTH / 2, -3 + GRIDHEIGHT / 2)
                self.draw_text(screen, "You : " + str(self.game.score), 30, white, -1 + GRIDWIDTH / 2, -3 + GRIDHEIGHT / 2)
                self.draw_text(screen, "Opp : "+str(self.game.opp_score), 30, white, 3+ GRIDWIDTH / 2, -3 + GRIDHEIGHT / 2)

                if not asked_for_rematch:
                    if self.game.n.check_if_opponent_asked_for_rematch():
                        self.draw_text(screen, "Opponent wants to rematch", 30, green, GRIDWIDTH / 2, -2+GRIDHEIGHT / 2)
                        if self.button(screen, "Accept", black, blue, -5 + GRIDWIDTH / 2, GRIDHEIGHT / 2, 4, 2):
                            opponent_player = self.game.n.check_if_opponent_is_ready(self.selected_player)
                            self.game.next_action = "PLAYGAME"
                            self.game.player.kill()
                            self.game.p2.kill()
                            self.game.opponent_player = int(opponent_player)
                            self.game.selected_player = self.selected_player
                            return

                        if self.button(screen, "Deny", black, blue, +5 + GRIDWIDTH / 2, GRIDHEIGHT / 2, 5, 2):
                            self.game.next_action = "Start"
                            self.game.player.kill()
                            self.game.p2.kill()
                            return
                    elif self.button(screen, "Ask for rematch", black, blue, GRIDWIDTH / 2, GRIDHEIGHT / 2, 8, 2):
                        asked_for_rematch = True
                else:
                    self.draw_text(screen, "Waiting for opponent response", 30, green, GRIDWIDTH / 2,GRIDHEIGHT / 2)
                    opponent_player = self.game.n.check_if_opponent_is_ready(self.selected_player)
                    if opponent_player:
                        pg.display.flip()
                        self.game.opponent_player = int(opponent_player)
                        self.game.selected_player = self.selected_player
                        self.game.next_action = "PLAYGAME"
                        self.game.player.kill()
                        self.game.p2.kill()
                        return


            # if player lost and is playing campaign
            else:
                self.game.player.update()
                self.game.platforms.update()
                self.game.all_sprites.draw(screen)
                self.draw_text(screen, "You Died !", 50, red, GRIDWIDTH/2, -4+GRIDHEIGHT/2)
                if level != 0:
                    if self.button(screen, "Try again", black, blue, GRIDWIDTH/2, 1+GRIDHEIGHT/2, 6, 2):
                        self.game.level = level
                        self.game.next_action = "PLAYGAME"
                        return

            if self.button(screen, "Menu", black, blue, GRIDWIDTH/2, 4+GRIDHEIGHT/2, 6, 2):
                self.game.next_action = "Start"
                self.game.player.kill()
                try:
                    if self.game.p2:
                        self.game.p2.kill()
                except:
                    pass
                return


            pg.display.flip()
            self.clock.tick(20)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.next_action = "QUIT"
                    self.game.menu_running = False
                    return
                if event.type == pg.KEYDOWN and finish and not self.game.multiplayer:
                    name += event.unicode
                    if event.key == pg.K_BACKSPACE:
                        name = name[:-2]

    def Pause(self, screen):
        run = True
        while run:
            self.game.all_sprites.draw(screen)
            self.draw_text(screen, "PAUSED", 50, blue, GRIDWIDTH / 2, -2 + GRIDHEIGHT / 2)
            if self.button(screen, "PLAY", black, blue, GRIDWIDTH / 2, 1 + GRIDHEIGHT / 2, 6, 2):
                time.sleep(0.2)
                return
            if self.button(screen, "Menu", black, blue, GRIDWIDTH / 2, 4 + GRIDHEIGHT / 2, 6, 2):
                self.game.next_action = "Start"
                self.game.playing = False
                return

            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.next_action = "QUIT"
                    self.game.menu_running = False
                    self.game.playing = False
                    return

    def Settings(self, screen):
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        screen.blit(self.image, (0, 0))
        fps = str(self.game.FPS)
        volume = str(self.game.volume)
        now = pg.time.get_ticks()
        is_modifying_fps = False
        is_modifying_volume = False
        is_modifying_left_key = False
        is_modifying_right_key = False
        is_modifying_jump_key = False
        left = pg.key.name(left_key)
        right = pg.key.name(right_key)
        jump = pg.key.name(jump_key)

        is_modifying = [is_modifying_fps,is_modifying_volume, is_modifying_left_key,is_modifying_right_key,is_modifying_jump_key]

        selected_knife = str(self.get_index_for(self.game.knife_image, knifesdict))


        run = True
        while run:
            screen.blit(self.image, (0, 0))

            # fps rate
            self.draw_text(screen, "FPS RATE : ", 30, white, 10, 5)
            self.text_box(screen,  fps, 15, 5, 3, 1.5, now, bar=is_modifying_fps)
            modify_fps = self.button(screen, "modify", white, black, 20, 5, 4, 1.5)
            if modify_fps:
                if not self.find_if_something_else_is_being_modified(is_modifying):
                    time.sleep(0.1)
                    is_modifying_fps = True
                elif is_modifying_fps:
                    time.sleep(0.1)
                    is_modifying_fps = False
            if self.check_for_errors(fps):
                self.draw_text(screen, "You have to enter a integer for fps", 30, red, 15, 16.5)

            # update is modifying list:
            is_modifying = [is_modifying_fps, is_modifying_volume, is_modifying_left_key, is_modifying_right_key,
                            is_modifying_jump_key]

            # volume
            self.text_box(screen, volume+"%", 15, 7, 3, 1.5, now, bar=is_modifying_volume)
            modify_volume = self.button(screen, "modify", white, black, 20, 7, 4, 1.5)
            self.draw_text(screen, "Volume : ", 30, white, 10, 7)
            if modify_volume:
                if not self.find_if_something_else_is_being_modified(is_modifying):
                    time.sleep(0.1)
                    is_modifying_volume = True
                elif is_modifying_volume:
                    time.sleep(0.1)
                    is_modifying_volume = False
            if self.check_for_errors(volume):
                self.draw_text(screen, "You have to enter a integer for volume", 30, red, 15, 16.5)

            # keys
            self.text_box(screen, left, 9, 10, 3, 1.5, now, bar=is_modifying_left_key)
            self.text_box(screen, right, 9, 12, 3, 1.5, now, bar=is_modifying_right_key)
            self.text_box(screen, jump, 9, 14, 3, 1.5, now, bar=is_modifying_jump_key)
            self.draw_text(screen, "Left key : ", 30, white, 5, 10)
            self.draw_text(screen, "Right key : ", 30, white, 5, 12)
            self.draw_text(screen, "Jump key : ", 30, white, 5, 14)
            modify_left_key = self.button(screen, "modify", white, black, 13, 10, 4, 1.5)
            if modify_left_key:
                if not self.find_if_something_else_is_being_modified(is_modifying):
                    time.sleep(0.1)
                    is_modifying_left_key = True
                elif is_modifying_left_key:
                    time.sleep(0.1)
                    is_modifying_left_key = False

            modify_right_key = self.button(screen, "modify", white, black, 13, 12, 4, 1.5)
            if modify_right_key:
                if not self.find_if_something_else_is_being_modified(is_modifying):
                    time.sleep(0.1)
                    is_modifying_right_key = True
                elif is_modifying_right_key:
                    time.sleep(0.1)
                    is_modifying_right_key = False

            modify_jump_key = self.button(screen, "modify", white, black, 13, 14, 4, 1.5)
            if modify_jump_key:
                if not self.find_if_something_else_is_being_modified(is_modifying):
                    time.sleep(0.1)
                    is_modifying_jump_key = True
                elif is_modifying_jump_key:
                    time.sleep(0.1)
                    is_modifying_jump_key = False



            # choose knife
            for i in range(1, len(knifesdict)+1):
                if str(i) == selected_knife:
                    self.draw_text(screen, "selected", 30, green, 450 + i * 100, 440, nogrid=True)
                if self.img_button(screen, knifesdict[str(i)], 430 + i * 100, 300, (40, 130), (45, 150)):
                    selected_knife = str(i)

            if self.return_to_menu(screen):
                if not self.check_for_errors(volume) and not self.check_for_errors(fps):
                    # update changed settings
                    if int(volume) != self.game.volume:
                        self.game.volume = int(volume)
                        self.game.sound_management("menu")
                    if int(fps) != self.game.FPS:
                        self.game.FPS = int(fps)
                    if knifesdict[str(selected_knife)] != self.game.knife_image:
                        self.game.knife_image = knifesdict[str(selected_knife)]
                    if pg.key.key_code(left) != self.game.left_key:
                        self.game.left_key = pg.key.key_code(left)
                    if pg.key.key_code(right) != self.game.right_key:
                        self.game.right_key = pg.key.key_code(right)
                    if pg.key.key_code(jump) != self.game.jump_key:
                        self.game.jump_key = pg.key.key_code(jump)
                self.game.next_action = "Start"
                return

            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.next_action = "QUIT"
                    self.game.menu_running = False
                    return
                if event.type == pg.KEYDOWN:
                    if is_modifying[0]: # FPS
                        fps += event.unicode
                        if event.key == pg.K_BACKSPACE:
                            fps = fps[:-2]
                    if is_modifying[1]: #volume
                        volume += event.unicode
                        if event.key == pg.K_BACKSPACE:
                            volume = volume[:-2]
                    if is_modifying_left_key: #left
                        left = event.unicode
                    if is_modifying_right_key: #left
                        right = event.unicode
                    if is_modifying_jump_key: #left
                        jump = event.unicode


    def Choose_player(self, screen):
        time.sleep(0.2)
        self.image = pg.transform.scale(Main_menubg, (screen_width, screen_height))
        screen.blit(self.image, (0, 0))
        selected_player = self.selected_player
        player_images = []
        for player in player_folders:
            image = pg.image.load(os.path.join(player[1], "Idle__000.png")).convert()
            player_images.append([image, player[0], self.find_reduction_coefficient(image, 200)])


        run = True
        while run:
            screen.blit(self.image, (0, 0))

            for i in range(len(player_images)):
                if i == selected_player:
                    self.draw_text(screen, "selected", 30, green, 170 + i * 200, 500, nogrid=True)
                self.draw_text(screen, player_images[i][1], 30, white, 150 + i * 200, 250, nogrid=True)
                image = player_images[i][0]
                red_coeff = player_images[i][2]
                if self.img_button(screen, image, 100 + i * 200, 300, (int(image.get_width()*red_coeff), int(image.get_height()*red_coeff)), (int(image.get_width()*(red_coeff+red_coeff*3/10)), int(image.get_height()*(red_coeff+red_coeff*3/10))), rotate=0):
                    selected_player = i


            if self.button(screen, "BACK", black, white, GRIDWIDTH/2, GRIDHEIGHT-2, 5, 2):
                time.sleep(0.2)
                return selected_player

            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.next_action = "QUIT"
                    self.game.menu_running = False
                    return "QUIT"


    ###################################################

    def ready_not_ready_button(self, screen, text, x, y, w, h):
        # This function creates a button on screen
        # it returns the text of the button if it is pressed, and none otherwise
        # changes the color of box when button is selected
        text_color = white
        x = x * TILESIZE
        y = y * TILESIZE
        w = w * TILESIZE
        h = h * TILESIZE
        mouse = pg.mouse.get_pos()
        rect = pg.rect.Rect(0, 0, w, h)
        rect.midtop = (x, y)
        if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
            button_color = light_grey
            pg.event.get()
            click = pg.mouse.get_pressed()
            if click[0] == 1:
                if self.ready_or_not == "ready":
                    self.ready_or_not = "not_ready"
                elif self.ready_or_not == "not_ready":
                    self.ready_or_not = "ready"
                self.game.sound_management("button_click")
                time.sleep(0.1)
        if self.ready_or_not == "ready":
            button_color = green
        else:
            button_color = red
            text = "not ready"
        pg.draw.rect(screen, button_color, rect)
        self.draw_text(screen, text, 30, text_color, x, 5 + y, True)

    def find_reduction_coefficient(self, image, goal_height):
        image = image
        rect = image_rect = image.get_rect()
        reduction_coefficient = 1
        if rect.h < goal_height:
            too_small = True
        else:
            too_small = False
        not_correct_size = True
        while not_correct_size:
            image = pg.transform.scale(image, (
                int(image_rect.w * reduction_coefficient), int(image_rect.h * reduction_coefficient)))
            rect = image.get_rect()
            if too_small:
                reduction_coefficient += 0.01
            if not too_small:
                reduction_coefficient -= 0.01

            if too_small and rect.h >= goal_height:
                not_correct_size = False
            if not too_small and rect.h <= goal_height:
                not_correct_size = False
        return reduction_coefficient

    def finished(self, highscore, screen, level, finish_time, name, now):
        self.draw_text(screen, "Well done !", 50, blue, GRIDWIDTH / 2, -5 + GRIDHEIGHT / 2)
        if not highscore:
            self.draw_text(screen, "Highscore : ", 30, red, 9 + GRIDWIDTH / 2, -5 + GRIDHEIGHT / 2)
            self.draw_text(screen, self.highscores[str(level)][0], 30, red, 9 + GRIDWIDTH / 2, -3 + GRIDHEIGHT / 2)
            self.draw_text(screen, self.highscores[str(level)][1] + "secs", 30, red, 9 + GRIDWIDTH / 2,
                           -2 + GRIDHEIGHT / 2)
        if not self.time_is_saved and highscore:
            self.draw_text(screen, "New Highscore !", 30, red, 9 + GRIDWIDTH / 2, -5 + GRIDHEIGHT / 2)
            self.draw_text(screen, str(finish_time) + "secs", 30, red, 9 + GRIDWIDTH / 2,
                           -3 + GRIDHEIGHT / 2)
            self.draw_text(screen, "Enter name to save highscore", 20, red, 9 + GRIDWIDTH / 2, -1 + GRIDHEIGHT / 2)
            self.text_box(screen, name, 9 + GRIDWIDTH / 2, GRIDHEIGHT / 2, 3, 2, now)
            if self.button(screen, "Save time", black, blue, 9 + GRIDWIDTH / 2, 3 + GRIDHEIGHT / 2, 6, 2):
                if len(name) > 0:
                    self.save_time(level, name, finish_time)
        if self.time_is_saved:
            self.draw_text(screen, "SAVED", 20, red, 9 + GRIDWIDTH / 2, -1 + GRIDHEIGHT / 2)

    def img_button(self, screen, image, x, y, small_size, big_size, rotate=-90):
        clicked = None
        image = pg.transform.rotate(image, rotate)
        image = pg.transform.scale(image, small_size)
        image = image.convert_alpha()
        small_rect = image.get_rect()
        small_rect.x = x
        small_rect.y = y
        mouse = pg.mouse.get_pos()
        if small_rect.x < mouse[0] < small_rect.x + small_rect.width and small_rect.y < mouse[1] < small_rect.y + small_rect.height:
            image = pg.transform.scale(image, big_size)
            big_rect = image.get_rect()
            click = pg.mouse.get_pressed()
            if click[0] == 1:
                clicked = True
                self.game.sound_management("button_click")
                time.sleep(0.1)
            screen.blit(image, (x-(big_rect.w-small_rect.w)/2, y-(big_rect.h-small_rect.h)/2))
        else:
            screen.blit(image, (x, y))
        return clicked

    def button(self, screen, text, button_color, text_color, x, y, w, h):
        # This function creates a button on screen
        # it returns the text of the button if it is pressed, and none otherwise
        # changes the color of box when mouse is hovering over it
        x = x * TILESIZE
        y = y * TILESIZE
        w = w * TILESIZE
        h = h * TILESIZE
        mouse = pg.mouse.get_pos()
        rect = pg.rect.Rect(0, 0, w, h)
        rect.midtop = (x, y)
        if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
            button_color = grey
            pg.event.get()
            click = pg.mouse.get_pressed()
            if click[0] == 1:
                self.game.sound_management("button_click")
                return text
        pg.draw.rect(screen, button_color, rect)
        self.draw_text(screen, text, 30, text_color, x, 5 + y, True)

    def draw_text(self, screen, text, size, color, x, y, nogrid=False, midtop=True):
        # This function draws text on screen, and dosen't return anything
        font = pg.font.Font(self.game.game_font, size)
        #font = pg.font.Font("/System/Library/Fonts/Supplemental/Arial.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if midtop:
            if not nogrid:
                text_rect.midtop = (x * TILESIZE, y * TILESIZE)
            if nogrid:
                text_rect.midtop = (x, y)
        else:
            if not nogrid:
                text_rect.topright = (x * TILESIZE, y * TILESIZE)
            if nogrid:
                text_rect.topright = (x, y)
        screen.blit(text_surface, text_rect)

    def text_box(self, screen, text, x, y, w, h, time, bar=True):
        # creates a text box with inputted text
        # makes box grow as text is growing
        # creates a vertical white bar to animate a bit
        x = x * TILESIZE
        y = y * TILESIZE
        w = w * TILESIZE
        h = h * TILESIZE
        font = pg.font.Font(self.game.game_font, 25)
        text_surface = font.render(text, True, white)
        self.text_width = text_surface.get_width()
        self.text_rect = text_surface.get_rect()
        self.text_rect.midtop = (x, 5 + y)

        if self.text_width + 40 > w:
            w = 40 + self.text_width
        rect = pg.rect.Rect(0, 0, w, h)
        rect.midtop = (x, y)
        pg.draw.rect(screen, black, rect)
        if bar:
            if (pg.time.get_ticks() - time) % 500 < 250:
                pg.draw.line(screen, white, (x + self.text_width / 2, y), (x + self.text_width / 2, y + 40), 3)

        screen.blit(text_surface, self.text_rect)

    def return_to_menu(self, screen):
        # This function creates a button for returning to menu,
        # returns next action if button is pressed
        restart = self.button(screen, "Return to menu", black, less_white, GRIDWIDTH/2, 18, 13, 2)
        if restart == "Return to menu":
            return restart

    def switch(self, screen, x, y, w, h, state, color):
        # this function creates a on/off switch, a bit like a radio button
        # returns the stated of the button: on or off
        # changes color when pressed
        mouse = pg.mouse.get_pos()
        rect = pg.rect.Rect(0, 0, w * TILESIZE, h * TILESIZE)
        rect.midtop = (x * TILESIZE, y * TILESIZE)
        pg.event.get()
        click = pg.mouse.get_pressed()

        if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height and click[0] == 1:
            self.game.sound_management("button_click")
            if not state:
                time.sleep(0.1)
                state = True
            else:
                time.sleep(0.1)
                state = False

        if state:
            text = "ON"
        else:
            text = "OFF"
            color = black

        pg.draw.rect(screen, color, rect)
        self.draw_text(screen, text, 30, white, x * TILESIZE, 5 + y * TILESIZE, True)
        return state

    def get_progress(self):
        file = open(progress_file, "r")
        self.levels_status = dict()
        for line in file:
            self.levels_status[line[0]] = line[2:].strip()
        file.close()

    def update_progress(self, level, status):
        file = open(progress_file, "r")
        lines = file.readlines()
        file = open(progress_file, "w")
        for line in lines:
            if line[0] == str(level):
                file.write(str(level)+": "+status+"\n")
            else:
                file.write(line)
        file.close()

    def get_highscores(self):
        file = open(highscores_file, "r")
        self.highscores = dict()
        for line in file:
            self.highscores[line[0]] = line[2:].strip().split(":")
        file.close()

    def save_time(self, level, name , time):
        file = open(highscores_file, "r")
        lines = file.readlines()
        file = open(highscores_file, "w")
        for line in lines:
            if line[0] == str(level):
                file.write(str(level) + ": " + name + ":" + str(time) + "\n")
            else:
                file.write(line)
        file.close()
        self.time_is_saved = True

    def draw_highscores(self, screen, x, y, w, h):

        # create table to insert values
        minisquare_width = int(w // 3)
        w = int(minisquare_width * 3)
        minisquare_height = int(h // (len(self.highscores) + 1))
        h = int(minisquare_height * (len(self.highscores) + 1))
        for i in range(x, x + w + minisquare_width, minisquare_width):  # vertical
            pg.draw.line(screen, white, (i, y), (i, h + y))
        for i in range(y, y + h + minisquare_height, minisquare_height):  # horizontal
            pg.draw.line(screen, white, (x, i), (x + w, i))

        # draw level numbers
        text_pos_y = y + 5 * minisquare_height / 4
        for i in range(1, len(self.highscores)+1):
            self.draw_text(screen, "Level " + str(i), 30, white, x + minisquare_width / 2, text_pos_y, nogrid=True)
            text_pos_y += minisquare_height

        # draw first line
        self.draw_text(screen, "Player", 30, white, x + 3*minisquare_width//2, y+minisquare_height//3, nogrid=True)
        self.draw_text(screen, "Time(secs)", 30, white, x + 5 * minisquare_width // 2, y + minisquare_height // 3,nogrid=True)


        # draw player names and scores
        text_pos_y = y + 5 * minisquare_height / 4
        for i in range(1, len(self.highscores) + 1):
            if self.highscores[str(i)][0]:
                self.draw_text(screen, self.highscores[str(i)][0], 30, red, x + 3*minisquare_width / 2, text_pos_y, nogrid=True)
                self.draw_text(screen, self.highscores[str(i)][1], 30, red, x + 5*minisquare_width / 2, text_pos_y, nogrid=True)

            else:
                self.draw_text(screen, "NONE", 30, blue, x + 3*minisquare_width / 2, text_pos_y, nogrid=True)
                self.draw_text(screen, "NONE", 30, blue, x + 5 * minisquare_width / 2, text_pos_y, nogrid=True)
            text_pos_y += minisquare_height

    def check_for_errors(self, supposedtobeaninteger):
        if len(supposedtobeaninteger) == 0:
            return True
        for caracter in supposedtobeaninteger:
            if "0" <= caracter <= "9":
                pass
            else:
                return True
        return False

    def find_if_something_else_is_being_modified(self, list, index=None):
        if index:
            for thing in list:
                if thing and thing != list[index]:
                    return True
            return False
        else:
            for thing in list:
                if thing:
                    return True
            return False

    def get_index_for(self, something, in_iterable):
        for i in range(1, len(in_iterable)):
            if something == in_iterable[str(i)]:
                return i



