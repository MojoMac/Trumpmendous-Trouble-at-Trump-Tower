import pygame as pg
from tile_pt1_settings import *
import random

class Spritesheet():
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename)
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width*2, height*2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y,  right_list, left_list, sprite_stand):

        self.groups = game.all_sprites

        pg.sprite.Sprite.__init__(self,self.groups) #pass self.groups

        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))

        #self.image.fill(RED)
        ### CHANGE self.image!!!!
        self.sprite_stand = sprite_stand
        self.sprite_stand.set_colorkey(BLACK)
        self.flip_stand = pg.transform.flip(sprite_stand, True, False)
        self.image = self.sprite_stand
        #self.mask = pg.mask.from_surface(self.image)


        self.vx, self.vy = 0, 0 #velocity values for both directions
        self.x = x * TILESIZE
        self.y = y *TILESIZE
        #self.playerpos = (self.x, self.y)
        self.gravity = PLAYERGRAV

        self.rect = self.image.get_rect()

        self.current_frame = 0
        self.delay = 50
        self.last = pg.time.get_ticks()
        self.right_list = right_list
        self.left_list = left_list

        self.run_left = False
        self.run_right = False

    #pg.sprite.collide_mask

    def collide_with_wall(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_trap(self):
        killed = pg.sprite.spritecollide(self, self.game.traps, False)
        if killed:
            self.kill()
            self.game.playing = False
    def collide_with_bottomlayer(self):
        killed = pg.sprite.spritecollide(self, self.game.bottomlayers, False)
        if killed:
            self.kill()
            hitsound.play()
            self.game.num = 1
            self.game.playing = False
    def collide_with_goal(self):
        won = pg.sprite.spritecollide(self, self.game.goals, False)
        if won:
            self.kill()

            self.game.num = 0
            self.game.playing = False


    def get_keys(self):
        self.vx = 0
        self.vy += self.gravity

        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT]:
            self.run_right = True
            self.now = pg.time.get_ticks()
            self.vx = PLAYERSPEED
            if self.now - self.last > self.delay:
                self.last = self.now
                self.current_frame =(self.current_frame+1)%len(self.right_list)

                self.image = self.right_list[self.current_frame]

        elif keys[pg.K_LEFT]:
            self.run_left = True
            self.now = pg.time.get_ticks()
            self.vx = -PLAYERSPEED
            if self.now - self.last > self.delay:
                self.last = self.now
                self.current_frame = (self.current_frame + 1) % len(self.left_list)

                self.image = self.left_list[self.current_frame]
        else:
            self.vx = 0
            if self.run_right:
                self.image = self.sprite_stand
                self.run_right = False
            elif self.run_left:
                self.image = self.flip_stand
                self.run_left = False


        #print (self.rect.x, self.rect.y)

    def jump(self):
        self.rect.y +=1
        hits = pg.sprite.spritecollide(self, self.game.walls, False,)
        self.rect.y -=1
        #if sprite collides
        if hits:
            self.vy= -13

    def update(self):
        self.get_keys()
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.collide_with_wall('x')
        self.rect.y = self.y
        self.collide_with_wall('y')
        self.collide_with_trap()
        self.collide_with_bottomlayer()
        self.collide_with_goal()

class Camera():
    def __init__(self,width,height):
        self.camera = pg.Rect(0,0,width,height)
        self.width = width
        self.height = height
    def get_view(self, sprite_object):
        #all sprite objects will be moved
        #based on the cameras updated position
        return sprite_object.rect.move(self.camera.topleft)
    def update(self,target):
        #shift the tile_map in the opposite direction of the target
        # adding half the window size to keep the target centered
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)

        #to stop scrolling when at the edge og the tile map
        # if the target moves too far left or up make x/y stay 0
        x = min(0,x)
        y = min(0,y)

        #if the target moves too far down or right make x/y stay at
        # the width of the tile-map minus the width of the window
        x = max(-1*(self.width - WIDTH), x)
        y = max(-1*(self.height - HEIGHT), y)

        #adjust the camera based on the new location
        self.camera = pg.Rect(x,y,self.width,self.height)

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls

        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = game.tileimg
        #self.image.fill(GREEN)

        self.game = game

        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Goal(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.goals

        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = game.goalimg

        self.game = game

        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Trap(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.traps

        pg.sprite.Sprite.__init__(self,self.groups)

        self.image = game.trapimg
        #self.image.fill(RED)

        self.game = game

        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class BottomLayer(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.bottomlayers

        pg.sprite.Sprite.__init__(self,self.groups)

        self.image = pg.Surface((1900,32))
        self.image = game.bottomlayerimg

        self.game = game

        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.x = self.x * 1900
        self.rect.y = self.y * TILESIZE
    def bottomLayermove(self):
        self.rect.y -= 1
    def update(self):
        self.bottomLayermove()
        #print(self.rect.x, self.rect.y)