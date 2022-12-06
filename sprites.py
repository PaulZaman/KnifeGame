#sprites classes
from settings import *



class Player(pg.sprite.Sprite):
    # This is the player sprite, created in createmap and update in main loop
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        # Add sprite to groups
        self.game.players.add(self)
        self.game.all_sprites.add(self)

        # animation and image
        self.animation_folder = self.game.player_folder
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.old_status = self.status = "idle"
        self.load_images()
        self.image = self.standing_frames[0].convert_alpha()
        self.reduction_coefficient = find_reduction_coefficient(self.image, 80)
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (int(self.image.get_width() *self.reduction_coefficient), int(self.image.get_height() *self.reduction_coefficient)))


        # deplacement
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # basic variables
        self.knife_counter = NUMBER_OF_KNIFES
        self.old_health = self.health = PLAYER_HEALTH
        self.last_shot = 0
        self.death_time = 0
        self.is_dead = False
        self.is_on = False
        self.old_is_on = False
        self.death_dir = 0
        self.rect.midbottom = self.pos

    def load_images(self):
        # this function loads image for player animation
        self.standing_frames = [pg.image.load(os.path.join(self.animation_folder, "Idle__000.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__001.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__002.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__003.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__004.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__005.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__006.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__007.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__008.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__009.png")).convert()
                                ]

        # running
        self.walk_frames_r = [pg.image.load(os.path.join(self.animation_folder, "Run__000.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__001.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__002.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__003.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__004.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__005.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__006.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__007.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__008.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__009.png")).convert()
                              ]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        # jumping
        self.jump_frames_r = [pg.image.load(os.path.join(self.animation_folder, "Jump__000.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__001.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__002.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__003.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__004.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__005.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__006.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__007.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__008.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__009.png")).convert()
                              ]
        self.jump_frames_l = []
        for frame in self.jump_frames_r:
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))

        # death
        self.death_frames_r = [pg.image.load(os.path.join(self.animation_folder, "Dead__000.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__001.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__002.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__003.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__004.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__005.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__006.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__007.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__008.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__009.png")).convert()
                              ]
        self.death_frames_l = []
        for frame in self.death_frames_r:
            self.death_frames_l.append(pg.transform.flip(frame, True, False))

    def animate(self):
        # this function animates the player sprite depending on it's status
        self.now = pg.time.get_ticks()
        self.old_status = self.status

        # this part is to determine status of player
        if self.vel.x != 0 and self.is_on:
            self.status = "walking"
        elif self.vel.y != 0 and not self.is_on:
            self.status = "jumping"
        elif self.vel.x == 0 and self.is_on:
            self.status = "idle"
        if self.pos.y > screen_height or self.health <= 0:
            self.status = "death"
            if self.current_frame == 9: # wait till player animation is done to pronouce player death
                self.is_dead = True
            # to determine wheather or not the player sprite should be killed,
            # or if the animation of death should be played
            if not self.death_time:
                self.death_time = pg.time.get_ticks()
                self.death_dir = self.vel.x
            if self.pos.y > screen_height:
                self.kill()
                self.is_dead = True

        # resets current frame counter if the status is different than the previous one
        if self.old_status != self.status:
            self.current_frame = 0

        # walk animation:
        if self.status == "walking":
            if self.now - self.last_update > 50:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame].convert_alpha()
                else:
                    self.image = self.walk_frames_l[self.current_frame].convert_alpha()
                self.rect.bottom = bottom
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image, (int(self.rect.w*self.reduction_coefficient), int(self.rect.h*self.reduction_coefficient)))
                self.rect = self.image.get_rect()

        # idle
        if self.status == "idle":
            if self.now - self.last_update > 50:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame].convert_alpha()
                self.rect.bottom = bottom
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image, (
                int(self.rect.w * self.reduction_coefficient), int(self.rect.h * self.reduction_coefficient)))
                self.rect = self.image.get_rect()

        # jumping
        if self.status == "jumping":
            if self.now - self.last_update > 50:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.jump_frames_r[self.current_frame].convert_alpha()
                else:
                    self.image = self.jump_frames_l[self.current_frame].convert_alpha()
                self.rect.bottom = bottom
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image, (
                int(self.rect.w * self.reduction_coefficient), int(self.rect.h * self.reduction_coefficient)))
                self.rect = self.image.get_rect()

        # player death
        if self.status == "death":
            if self.now - self.last_update > 120:
                self.last_update = self.now
                if self.current_frame != 9:
                    self.current_frame = (self.current_frame + 1) % len(self.death_frames_l)
                bottom = self.rect.bottom
                if self.death_dir >= 0:
                    self.image = self.death_frames_r[self.current_frame].convert_alpha()
                else:
                    self.image = self.death_frames_l[self.current_frame].convert_alpha()
                self.rect.bottom = bottom
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image, (
                    int(self.rect.w * self.reduction_coefficient), int(self.rect.h * self.reduction_coefficient)))
                self.rect = self.image.get_rect()

    def update(self):
        # updates player sprite at each main loop iteration

        # manage sound for landing on platforms / health
        if self.old_is_on != self.is_on and self.is_on:
            self.game.sound_management("land_on_plat")
        if self.old_health != self.health:
            self.game.sound_management("hit")

        self.apply_motion_eq()
        self.block_player_on_sides()
        self.animate()

        self.rect.midbottom = self.pos
        self.old_is_on = self.is_on
        self.old_health = self.health
        #self.health = 3

    def check_key_pressed(self):
        # checks if user input is detected, and applies corresponding action

        keys = pg.key.get_pressed()
        if keys[self.game.left_key]:
            self.acc.x = -PLAYER_ACC
        if keys[self.game.right_key]:
            self.acc.x = +PLAYER_ACC
        if keys[self.game.jump_key]:
            self.jump()

        mouse = pg.mouse.get_pressed()
        if mouse[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot > KNIFE_RATE and self.knife_counter > 0:
                    mouse_pos = pg.mouse.get_pos()
                    if mouse_pos[0]>60 or mouse_pos[1]>60:
                        self.throw_knife(self.pos, mouse_pos)

    def apply_motion_eq(self):
        self.acc = vec(0, PLAYER_GRAV)
        if self.status != "death":
            self.check_key_pressed()

        # motion equations
        self.acc.x += self.vel.x * PLAYER_FRICTION  # friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if abs(self.vel.x) < 0.3:   # stops player if velocity is too low
            self.vel.x = 0

        if self.vel.y > 11: # limits player fall speed
            self.vel.y = 11

    def block_player_on_sides(self):
        # block player on sides exept if player is exiting a level

        if self.pos.x + (self.rect.width / 2) > screen_width:
            self.pos.x = screen_width - (self.rect.width / 2)
        if self.game.level == 1 and 330 < self.rect.y < 420:
            pass
        elif self.game.level == 2 and 428 < self.rect.y < 500 and self.game.game_status == "openned" and self.game.all_guards_are_dead:
            pass
        elif self.game.level == 3 and 428 < self.rect.y < 500 and self.game.all_guards_are_dead:
            pass
        elif self.game.level == 4 and self.rect.y < 100:
            pass
        elif self.game.level == 5 and self.rect.y < 100:
            pass
        elif self.pos.x - (self.rect.width / 2) < 0:
            self.pos.x = (self.rect.width / 2)

    def throw_knife(self, pos, mouse_pos):
        # called when player clicks on mouse to shoot a knife
        self.game.sound_management("knife_throw")
        self.knife_counter -= 1
        self.last_shot = pg.time.get_ticks()
        Knife(self.game, pos, mouse_pos, self)

    def jump(self):
        # called when user asks player to jump
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if self.is_on and hits:
            self.game.sound_management("jump")
            self.vel.y = JUMP_HEIGHT
            self.is_on = False


class Opponent_multi(pg.sprite.Sprite):
    # this is the sprite corresponding to the opponent when playing multiplayer
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.all_sprites.add(self)

        # load/initialize images
        self.animation_folder = player_folders[self.game.opponent_player][1]
        self.load_images()
        self.image = self.standing_frames[0].convert_alpha()
        self.reduction_coefficient = find_reduction_coefficient(self.image, 80)
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (int(self.image.get_width() * self.reduction_coefficient),
                                                     int(self.image.get_height() * self.reduction_coefficient)))

        # opponent variables
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.old_pos = vec(0, 0)
        self.status = "idle"
        self.is_dead = False
        self.current_frame = 0
        self.old_status = 0
        self.last_update = 0
        self.health = GUARD_HEALTH
        self.death_dir = 0
        self.death_time = None

    def update(self):
        # updates position and animates sprite
        self.animate()
        self.rect.midbottom = self.pos
        self.old_pos = self.pos

    def load_images(self):
        # load images for opponent animation

        self.standing_frames = [pg.image.load(os.path.join(self.animation_folder, "Idle__000.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__001.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__002.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__003.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__004.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__005.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__006.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__007.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__008.png")).convert(),
                                pg.image.load(os.path.join(self.animation_folder, "Idle__009.png")).convert()
                                ]

        # running
        self.walk_frames_r = [pg.image.load(os.path.join(self.animation_folder, "Run__000.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__001.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__002.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__003.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__004.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__005.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__006.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__007.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__008.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Run__009.png")).convert()
                              ]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        # jumping
        self.jump_frames_r = [pg.image.load(os.path.join(self.animation_folder, "Jump__000.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__001.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__002.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__003.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__004.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__005.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__006.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__007.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__008.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Jump__009.png")).convert()
                              ]
        self.jump_frames_l = []
        for frame in self.jump_frames_r:
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))

        # death
        self.death_frames_r = [pg.image.load(os.path.join(self.animation_folder, "Dead__000.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__001.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__002.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__003.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__004.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__005.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__006.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__007.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__008.png")).convert(),
                              pg.image.load(os.path.join(self.animation_folder, "Dead__009.png")).convert()
                              ]
        self.death_frames_l = []
        for frame in self.death_frames_r:
            self.death_frames_l.append(pg.transform.flip(frame, True, False))

    def animate(self):
        # animates opponent
        self.now = pg.time.get_ticks()
        self.old_status = self.status

        # find velocity vector for animation
        self.vel[0] = self.pos[0] - self.old_pos[0]
        self.vel[1] = self.pos[1] - self.old_pos[1]

        # this part is to determine status of player
        if self.vel.x != 0 and self.vel.y == 0:
            self.status = "walking"
        elif self.vel.y != 0 and not self.vel.y == 0:
            self.status = "jumping"
        elif self.vel.x == 0 and self.vel.y == 0:
            self.status = "idle"
        if self.pos[1] > screen_height or self.health <= 0:
            self.status = "death"
            if self.current_frame == 9:  # wait till player animation is done to pronouce player death
                self.is_dead = True
            # to determine wheather or not the player sprite should be killed,
            # or if the animation of death should be played
            if not self.death_time:
                self.death_time = pg.time.get_ticks()
                self.death_dir = self.vel.x
            if self.pos[1] > screen_height:
                self.kill()
                self.is_dead = True

        # resets current frame counter if the status is different than the previous one
        if self.old_status != self.status:
            self.current_frame = 0

        # walk animation:
        if self.status == "walking":
            if self.now - self.last_update > 50:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame].convert_alpha()
                else:
                    self.image = self.walk_frames_l[self.current_frame].convert_alpha()
                self.rect.bottom = bottom
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image, (int(self.rect.w*self.reduction_coefficient), int(self.rect.h*self.reduction_coefficient)))
                self.rect = self.image.get_rect()

        # idle
        if self.status == "idle":
            if self.now - self.last_update > 50:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame].convert_alpha()
                self.rect.bottom = bottom
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image, (
                int(self.rect.w * self.reduction_coefficient), int(self.rect.h * self.reduction_coefficient)))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # jumping
        if self.status == "jumping":
            if self.now - self.last_update > 50:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.jump_frames_r[self.current_frame].convert_alpha()
                else:
                    self.image = self.jump_frames_l[self.current_frame].convert_alpha()
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image, (
                    int(self.rect.w * self.reduction_coefficient), int(self.rect.h * self.reduction_coefficient)))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # player death
        if self.status == "death":
            if self.now - self.last_update > 120:
                self.last_update = self.now
                if self.current_frame != 9:
                    self.current_frame = (self.current_frame + 1) % len(self.death_frames_l)
                bottom = self.rect.bottom
                if self.death_dir >= 0:
                    self.image = self.death_frames_r[self.current_frame].convert_alpha()
                else:
                    self.image = self.death_frames_l[self.current_frame].convert_alpha()
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image, (
                    int(self.rect.w * self.reduction_coefficient), int(self.rect.h * self.reduction_coefficient)))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def draw_life(self):
        # draw life counter for opponent
        for i in range(self.health):
            image = pg.transform.scale(life_image.convert().convert_alpha(), (10, 10))
            self.game.screen.blit(image, (self.pos[0]-15 + 15*i, self.rect.y-15))


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, collisions):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.platforms.add(self)
        #self.game.all_sprites.add(self)
        self.image = pg.Surface([TILESIZE, TILESIZE])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.mask = pg.mask.from_surface(self.image)
        #self.image.fill(red)
        #self.rect = self.image.get_rect()
        self.collisions = collisions
        self.bottom_colliding = False
        self.top_colliding = False
        self.side_colliding = False
        self.game = game

    def update(self):


        if self.collisions == '-':
            self.top_collisions2()

        if self.collisions == 'a':
            self.top_collisions()
            self.bottom_collisions()
            self.side_collisions()

        if self.collisions == "i":
            self.side_collisions()

    def top_collisions(self):
        self.top_colliding = False
        self.game.player.rect.y += 1
        if pg.sprite.collide_rect(self.game.player, self) and self.rect.y + 10 > self.game.player.rect.bottom:
            self.game.colliding_platforms.append((self.rect.x, self.rect.y))
        self.game.player.rect.y -= 1
        if self.game.player.vel.y > 0:
            for plat in self.game.colliding_platforms:
                if plat[0]-5 <= self.game.player.pos.x <= plat[0] + 35:
                    self.game.player.pos.y = plat[1]
                    self.game.player.vel.y = 0
                    self.game.player.is_on = True
                    self.top_colliding = True

    def top_collisions2(self):
        self.top_colliding = False
        self.game.player.rect.y += 10
        if pg.sprite.collide_rect(self.game.player, self) and self.game.player.rect.y+self.game.player.rect.h < self.rect.y + self.rect.h and self.game.player.vel.y>0:
            if self.rect.x - 5 <= self.game.player.pos.x <= self.rect.x + 35:
                self.game.player.pos.y = self.rect.y
                self.game.player.vel.y = 0
                self.game.player.is_on = True
                self.top_colliding = True
        self.game.player.rect.y -= 10

    def side_collisions(self):
        self.side_colliding = False
        if not self.top_colliding and not self.bottom_colliding:
            if self.game.player.vel.x > 0:
                self.game.player.rect.x += 1
            elif self.game.player.vel.x < 0:
                self.game.player.rect.x -= 1

            if pg.sprite.collide_rect(self.game.player, self):
                if self.game.player.rect.y+5<self.rect.y<self.game.player.pos.y-5 or self.game.player.rect.y+5<self.rect.y+self.rect.w<self.game.player.pos.y-5:
                    if self.game.player.rect.x  < self.rect.x:
                        if self.game.player.vel.x > 0:
                            self.game.player.pos.x = self.rect.x - self.game.player.rect.w / 2
                            self.game.player.vel.x = 0
                            self.game.player.is_on = False
                            self.side_colliding = True
                    if self.game.player.rect.x+self.game.player.rect.w > self.rect.x + self.rect.w:
                        if self.game.player.vel.x < 0:
                            self.game.player.pos.x = self.rect.x + self.rect.w + self.game.player.rect.w / 2
                            self.game.player.vel.x = 0
                            self.game.player.is_on = False
                            self.side_colliding = True

            if self.game.player.vel.x > 0:
                self.game.player.rect.x -= 1
            elif self.game.player.vel.x < 0:
                self.game.player.rect.x += 1

    def bottom_collisions(self):
        self.bottom_colliding = False
        if not self.side_colliding and not self.top_colliding and not self.game.player.is_on:
            if self.game.player.vel.y < 0:
                self.game.player.rect.y -= 1
                if pg.sprite.collide_rect(self.game.player, self):
                    if self.game.player.rect.x+3<self.rect.x+self.rect.w<self.game.player.rect.x+self.game.player.rect.w-3 or self.game.player.rect.x+3<self.rect.x<self.game.player.rect.x+self.game.player.rect.w-3:
                        if self.game.player.rect.y>self.rect.y:
                            self.game.player.pos.y = self.rect.y+self.rect.h+self.game.player.rect.h
                            self.game.player.vel.y = 0
                self.game.player.rect.y += 1


class Cell(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.load_images()
        self.game.all_sprites.add(self)
        self.image = self.doors[0].convert_alpha()
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0
        self.looted = False
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def load_images(self):
        self.doors = []
        for i in range(13):
            i += 1
            self.doors.append(pg.image.load(os.path.join(celldoor_folder, celldict[str(i)])).convert())

    def open(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            center = self.rect.center
            if self.current_frame < 12:
                self.current_frame = self.current_frame+1
            self.image = self.doors[self.current_frame].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = center
            if self.current_frame == 12 and not self.looted:
                self.game.game_status = "openned"
                self.game.player.knife_counter = 3
                self.looted = True

    def update(self):
        hits = pg.sprite.spritecollideany(self, self.game.players)
        if hits:
            self.open()


class Guard(pg.sprite.Sprite):
    def __init__(self, game, x, y, status="walking"):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.status = status

        # animation
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        if self.status == "idle":
            self.image = self.standing_frames[0].convert_alpha()
            self.image = pg.transform.scale(self.image, (40, 75))
        else:
            self.image = self.walk_frames_l[0].convert_alpha()
            self.image = pg.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
        if self.game.level != 4:
            self.game.all_sprites.add(self)
        self.game.guards.add(self)

        self.pos = vec(x*TILESIZE, 30+y*TILESIZE)
        self.life = 2
        self.vel = random.randrange(-1, 1, 2) * GUARD_SPEED

        self.rect.midbottom = self.pos
        self.ray = Ray(self.game)
        self.shoot_time = 0

    def update(self):
        if self.status != 'death':
            self.ray.update(self.pos, self.game.player.pos)
            if self.ray.nothing_there:
                self.shoot()

            if pg.sprite.spritecollideany(self, self.game.platforms) or not self.check_if_plat_is_underneath():
                self.vel *= -1

            hits = pg.sprite.spritecollideany(self, self.game.knifes)

            if hits:
                if hits.vel != (0,0):
                    self.life -= 1
                hits.kill()
            self.animate()
            if self.life <= 0:
                Knife(self.game, self.pos, [self.rect.x, self.rect.y], self.game.player, velocity=1)
                Knife(self.game, self.pos, [self.rect.x+self.rect.w, self.rect.y], self.game.player, velocity=1)
                Knife(self.game, self.pos, [self.pos[0], self.pos[1]-self.rect.h], self.game.player, velocity=1)
                self.status = "death"
                self.game.n_of_dead_guards += 1
            if self.status == "walking":
                self.pos.x += self.vel
            self.rect.midbottom = self.pos

        else:
            self.animate()


    def check_if_plat_is_underneath(self):
        self.rect.x += self.vel*30
        self.rect.y += 30
        if not pg.sprite.spritecollideany(self, self.game.platforms):
            self.rect.x -= self.vel * 30
            self.rect.y -= 30
            return False
        self.rect.x -= self.vel * 30
        self.rect.y -= 30
        return True

    def load_images(self):
        self.standing_frames = [pg.image.load(os.path.join(guard_animation_folder, "Static0.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static1.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static2.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static3.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static4.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static5.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static6.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static7.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static8.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static9.png")).convert(),
                                pg.image.load(os.path.join(guard_animation_folder, "Static10.png")).convert(),
                                ]

        # running
        self.walk_frames_r = [pg.image.load(os.path.join(guard_animation_folder, "run1.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "run2.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "run3.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "run4.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "run5.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "run6.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "run7.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "run8.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "run9.png")).convert()
                              ]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))


        # death
        self.death_frames_r = [pg.image.load(os.path.join(guard_animation_folder, "death0.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death1.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death2.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death3.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death4.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death5.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death6.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death7.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death8.png")).convert(),
                              pg.image.load(os.path.join(guard_animation_folder, "death9.png")).convert()
                              ]
        self.death_frames_l = []
        for frame in self.death_frames_r:
            self.death_frames_l.append(pg.transform.flip(frame, True, False))

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.shoot_time > 600:
            Bullet(self.game, self.pos, self.game.player.pos)
            self.shoot_time = pg.time.get_ticks()

    def animate(self):
        self.now = pg.time.get_ticks()
        # walk animation:
        if self.status == "walking":
            if self.now - self.last_update > 50:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.midbottom
                if self.vel > 0:
                    self.image = self.walk_frames_r[self.current_frame].convert_alpha()
                else:
                    self.image = self.walk_frames_l[self.current_frame].convert_alpha()
                self.rect.midbottom = bottom
                self.image = pg.transform.scale(self.image, (50, 70))
                self.rect = self.image.get_rect()

        # idle
        if self.status == "idle":
            if self.now - self.last_update > 50:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame].convert_alpha()
                self.rect.bottom = bottom
                self.image = pg.transform.scale(self.image, (40, 75))
                self.rect = self.image.get_rect()

        # death
        if self.status == "death":
            if self.now - self.last_update > 120:
                self.last_update = self.now
                if self.current_frame != 9:
                    self.current_frame = (self.current_frame + 1) % len(self.death_frames_l)
                bottom = self.rect.bottom
                if self.vel > 0:
                    self.image = self.death_frames_r[self.current_frame].convert_alpha()
                else:
                    self.image = self.death_frames_l[self.current_frame].convert_alpha()
                self.rect.bottom = bottom
                self.image = pg.transform.scale(self.image, (66, 80))
                self.rect = self.image.get_rect()
                self.rect.midbottom = self.pos


class Ray(pg.sprite.Sprite):
    def __init__(self, game):
            pg.sprite.Sprite.__init__(self)
            self.game = game
            self.ray_image = pg.image.load(os.path.join(img_folder, "rayy.png")).convert()
            self.ray_image.set_colorkey(black)


    def update(self, start_pos, end_pos):
        self.nothing_there = False
        self.start_pos = (start_pos[0], start_pos[1] - 30)
        self.end_pos = (end_pos[0], end_pos[1] - 30)
        self.pos = vec(self.start_pos)
        self.dir = vec(self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1])
        self.image = pg.transform.scale(self.ray_image, [abs(int(self.dir[0])), abs(int(self.dir[1])) + 5])

        if self.end_pos[0] < self.start_pos[0]:
            self.image = pg.transform.flip(self.image, True, False)
            self.pos[0] = self.end_pos[0]
            if self.end_pos[1] < self.start_pos[1]:
                self.image = pg.transform.flip(self.image, False, True)
                self.pos[1] = self.end_pos[1]
        elif self.end_pos[0] > self.start_pos[0]:
            if self.end_pos[1] < self.start_pos[1]:
                self.image = pg.transform.flip(self.image, False, True)
                self.pos[0] = self.start_pos[0]
                self.pos[1] = self.end_pos[1]

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
        pg.Surface.blit(self.game.screen, self.image, self.rect)
        self.mask = pg.mask.from_surface(self.image)
        if not self.check_for_platforms():
            self.nothing_there = True


    def check_for_platforms(self):
        if self.start_pos[0]-5<self.end_pos[0]< self.start_pos[0]+5:
            return True
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:
            if pg.sprite.collide_mask(self, hit):
                return True
        return False


class Camera(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.game = game
        self.game.all_sprites.add(self)
        self.cam_image = pg.image.load(os.path.join(img_folder, "cam.png")).convert()
        self.cam_image = pg.transform.scale(self.cam_image, (30, 30))
        self.ray = Ray(self.game)
        self.image = self.cam_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = vec(self.x+15, self.y+15)
        self.fov_pos = vec(self.x+15, self.y+15)
        self.direction = vec(800, 0)
        self.rect.center = self.pos
        self.rotation = -1
        self.angle = -90
        self.alarm = False

    def update(self):
        if not self.alarm:
            self.ray.update(self.pos, self.game.player.pos)
            if self.angle-2<-self.ray.dir.angle_to(vec(1, 0))<self.angle+2 and self.ray.nothing_there:
                self.alarm = True
        if self.angle < -230 or self.angle > -10:
            self.rotation *= -1
        self.angle += self.rotation
        self.image = self.rot_center(self.cam_image, -self.angle)

    def draw_camera_field(self):
        pg.draw.line(self.game.screen, red, self.fov_pos, self.fov_pos + self.direction.rotate(self.angle), 3)
        pg.display.flip()

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, guard_pos, player_pos, velocity=5):
            pg.sprite.Sprite.__init__(self)
            self.game = game
            self.game.all_sprites.add(self)
            self.image = pg.image.load(os.path.join(img_folder, "bullet.png")).convert().convert_alpha()
            self.image = pg.transform.scale(self.image, (30, 15))
            self.image_without_rotation = self.image
            self.rect = self.image.get_rect()
            self.guard_pos = guard_pos
            self.player_pos = player_pos
            self.vel = velocity
            self.pos = vec(self.guard_pos[0], self.guard_pos[1]-60)
            self.dir = vec(self.player_pos[0]-self.guard_pos[0], self.player_pos[1]-self.guard_pos[1]).normalize()
            self.rect.center = self.pos

    def update(self):
            self.pos += self.dir*self.vel
            if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height or pg.sprite.spritecollideany(self, self.game.platforms):
                self.kill()
            if pg.sprite.collide_rect(self, self.game.player):
                self.kill()
                self.game.player.health -= 1
            self.update_rotation()
            self.rect.center = self.pos

    def update_rotation(self):
        self.angle = self.dir.angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.image_without_rotation, self.angle)


class Knife(pg.sprite.Sprite):
    def __init__(self, game, player_pos, mouse_pos, player, velocity=5, ennemy_knife=False):
            pg.sprite.Sprite.__init__(self)
            self.player = player
            self.game = game

            self.game.knifes.add(self)
            self.game.all_sprites.add(self)

            self.image = self.game.knife_image.convert().convert_alpha()
            self.image = pg.transform.scale(self.image, (30, 20))
            self.image_without_rotation = self.image
            self.rect = self.image.get_rect()
            self.knifeimage = self.image

            self.image_rotation_angle = 0
            self.player_pos = player_pos
            self.mouse_pos = mouse_pos
            self.x_mouse, self.y_mouse = mouse_pos
            self.vel = velocity
            self.previous_pos = self.player_pos
            self.mouse_to_player = vec(self.mouse_pos[0] - self.player_pos[0], self.mouse_pos[1] - self.player_pos[1])
            self.mouse_to_player = self.mouse_to_player.normalize()
            self.angle = self.mouse_to_player.angle_to(vec(1, 0))
            self.initial_time = pg.time.get_ticks()  # clock, necessary to implement time equations
            self.pos = (self.player_pos[0], self.player_pos[1]-60)  # initial position of the knife
            self.angle /= 18 * math.pi  # convert angle to radians
            self.x, self.y = self.pos  # initial x and y of the position of the knife
            self.rotation_update()

    def update(self):

            self.now = pg.time.get_ticks()
            if not pg.sprite.spritecollideany(self, self.game.platforms):
                x_buffer = KNIFE_SPEED * (math.cos(self.angle)) * (self.now - self.initial_time) / 25 + self.x  # necessary in order to avoiding modify the initial x
                #   x    =     v0     *     cos(alpha)     *              t                   + c
                y_buffer = KNIFE_GRAV * ((self.now - self.initial_time) / 25) ** 2 / 2 + KNIFE_SPEED * -math.sin(self.angle) * ( self.now - self.initial_time) / 25 + self.y  # necessary for the same reasons
                #   y    =    -g      *     t²         / 2 +   y0    *   sin(alpha)     *      t  +   c'
                self.pos = (x_buffer, y_buffer)
                self.rotation_update()
            else:
                self.vel = 0

            # self.collision_with_walls()
            # self.collision_with_opponent()
            self.collision_with_self()
            self.collision_with_opponent()
            self.rect.center = self.pos

            self.mask = pg.mask.from_surface(self.image)

    def rotation_update(self):
        self.velocity = vec(self.previous_pos[0] - self.pos[0], self.previous_pos[1] - self.pos[1])
        self.image_rotation_angle = self.velocity.angle_to(vec(1, 0)) + 180
        self.image = pg.transform.rotate(self.image_without_rotation, self.image_rotation_angle)
        self.previous_pos = self.pos

    def collision_with_opponent(self):
        # if the player's knife hits ennemy
        try:
            hits = pg.sprite.collide_rect(self, self.game.p2)
            if hits:
                self.kill()
        except:
            pass

    def collision_with_self(self):
        if self.now - self.initial_time > 200:
            hits = pg.sprite.collide_rect(self, self.game.player)
            if hits:
                self.kill()
                self.game.player.knife_counter += 1

    def collision_with_walls(self):
        # not really ressource efficient this one
        for wall in self.game.walls:
            hits = pg.sprite.collide_rect(self, wall)
            if hits:
                if self.vel != (0, 0):
                    self.stop_rotation = self.vel
                    self.angle = -(vec(1, 0).angle_to(self.stop_rotation))
                self.vel = vec(0, 0)
                return True


class Ennemy_Knife(pg.sprite.Sprite):
    def __init__(self, game, pos, angle):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.opp_knifes.add(self)
        self.game.all_sprites.add(self)
        self.image = self.game.knife_image.convert().convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 20))
        self.rect = self.image.get_rect()
        self.knifeimage = self.image
        self.pos = pos
        self.rect.center = self.pos
        self.throw_time = pg.time.get_ticks()
        self.angle = angle

    def update(self):
        self.now = pg.time.get_ticks()
        self.image = pg.transform.rotate(self.knifeimage, self.angle)
        self.rect.center = self.pos
        self.collision_with_player()

    def collision_with_player(self):
        hitsplat = pg.sprite.spritecollideany(self, self.game.platforms)
        hits = pg.sprite.spritecollideany(self, self.game.players)
        if hits:
            if not hitsplat:
                self.game.player.health -= 1
            self.game.player.knife_counter += 1
            self.kill()


class Knife_box(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        if self.game.level != 4:
            self.game.all_sprites.add(self)
        self.game.supplements.add(self)
        self.image = knife_box_image.convert().convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x * 30
        self.rect.y = y * 30
        self.drawn_on_screen=False

    def update(self):
        if pg.sprite.collide_rect(self.game.player, self):
            self.game.player.knife_counter += 3
            self.kill()
        if self.game.game_status == "normalview" and not self.drawn_on_screen:
            self.game.all_sprites.add(self)
            self.drawn_on_screen = True


class Life_bonus(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.supplements.add(self)
        if self.game.level != 4:
            self.game.all_sprites.add(self)
        self.image = life_image.convert().convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x * 30
        self.rect.y = y * 30
        self.drawn_on_screen = False

    def update(self):
        if pg.sprite.collide_rect(self.game.player, self):
            self.game.player.health = 3
            self.kill()
        if self.game.game_status == "normalview" and not self.drawn_on_screen:
            self.game.all_sprites.add(self)
            self.drawn_on_screen = True


class Key(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.all_sprites.add(self)
        self.image = key_image.convert().convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x * 30
        self.rect.y = y * 30

    def update(self):
        if pg.sprite.collide_rect(self.game.player, self):
            self.game.game_status = "got_the_key"
            self.kill()



def find_reduction_coefficient(image, goal_height):
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