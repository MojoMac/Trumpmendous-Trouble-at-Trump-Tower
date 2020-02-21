import pygame as pg
import tile_pt1_sprites as gs
from tile_pt1_settings import *

class Game():
    def __init__(self):
        #initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Get Jiggy with it')
        self.clock = pg.time.Clock()
        self.running = True
        self.load()
    def load(self):
        self.tileimg = pg.transform.scale(TILEIMG, (32, 32))
        self.trapimg = pg.transform.scale(TRAPIMG, (32,32))
        self.goalimg = pg.transform.scale(ENDGOALIMG, (32,32))
        self.bottomlayerimg = pg.transform.scale(BOTTOMLAYERIMG, (1900, 1900))
        self.bg = pg.image.load(MAPIMG)
        pg.mixer.music.load('Manuel - Gas Gas Gas 8Bit.mp3')
        pg.mixer.music.set_endevent(pg.constants.USEREVENT)
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play()

        #self.player_img = pg.image.load(PLAYERIMG).convert()
        #self.wall_img = pg.image.load( ).convert

    def new(self):
        '''create all game objects, sprites, and sprite groups and call run'''

        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.traps = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        self.bottomlayers = pg.sprite.Group()
        # creating instance of the camera class using MAPWIDTH and MAPHEIGHT from settings
        self.game_viewer = gs.Camera(MAPWIDTH, MAPHEIGHT)
        player_sheet = gs.Spritesheet('trump_runmap.png')
        playerright_list = []
        for x in range(6):
            image = player_sheet.get_image(100 * x + 35, 111, 59, 78) #35, 111 to 94, 189; 59 by 78 squares
            image1 = pg.transform.scale(image, (50,64))
            image1.set_colorkey(BLACK)
            playerright_list.append(image1)

        playerleft_list = []
        for image in playerright_list:
            playerleft_list.append(pg.transform.flip(image, True, False))
            image.set_colorkey(BLACK)
        playerimg = player_sheet.get_image(100 * x + 35, 111, 59, 78)
        playerimg1 = pg.transform.scale(playerimg,(50,64))

        for row, pattern in enumerate(TILEMAP1):
            for col, tile in enumerate(pattern):
                if tile == '1':
                    gs.Wall(self,col,row)
                if tile == 'x':
                    gs.Trap(self,col,row)
                if tile == 'g':
                    gs.Goal(self,col,row)
                if tile == 'p':
                    self.player = gs.Player(self, col, row,playerright_list,playerleft_list,playerimg1)
        gs.BottomLayer(self, 0, 92)

        self.run()

    def run(self):
        '''contains main game loop'''
        self.playing = True
        self.num = 1

        while self.playing:
            self.clock.tick(FPS)
            #print(self.clock.get_fps())
            self.events()
            self.update()
            self.draw()



    def update(self):
        #update sprites, etc
        self.all_sprites.update()

        #update the viewer with the player passed in as the target
        self.game_viewer.update(self.player)

    def draw(self):
        '''fill screen, draw objects, sprites to the display, and flip'''
        self.screen.fill(BLACK)
        #self.draw_grid()
        self.screen.blit(self.bg, (0,0))
        #camera requires blitting rather than calling all_sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.game_viewer.get_view(sprite))
        pg.display.flip()

    def events(self):
        # game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.running = False
            #jumping handled here to keep player
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def show_start_screen(self):
        # screen to start game
        #print(pg.font.get_fonts())
        pg.init()
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        clock = pg.time.Clock()

        font = pg.font.SysFont('Impact', 30, False, False)
        font2 = pg.font.SysFont('Impact', 120, False, False)
        font3 = pg.font.SysFont('Impact', 60, False, False)
        start_text1 = 'Press Enter to start'
        start_text2 = 'or ESC to exit'
        trump = 'TRUMPMENDOUS'
        bground = pg.image.load('the floor is lava.jpg')

        text1 = font.render(start_text1, True, RED)
        text1rect = text1.get_rect()
        text1rect.midtop = (1115, 400)
        text2 = font.render(start_text2, True, RED)
        text2rect = text2.get_rect()
        text2rect.midtop = (140, 400)
        trumptext = font2.render(trump, True, BLUE)
        text3rect = trumptext.get_rect()
        text3rect.midtop = (640, 200)
        startgame = False

        while not startgame:

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    startgame = True
            screen.fill(WHITE)
            screen.blit(bground, [0, 0])
            screen.blit(text1, text1rect)
            screen.blit(text2, text2rect)
            screen.blit(trumptext, text3rect)

            pg.display.flip()

            clock.tick(FPS)
        #pass

    def decide_screen(self):
        if self.num == 1:
            #self.playing = False
            game.show_go_screen()
        if self.num == 0:
            #self.playing = False
            game.show_win_screen()


    def show_go_screen(self):
        # screen when game over
        pg.init()
        go_screen = pg.display.set_mode((WIDTH, HEIGHT))
        clock = pg.time.Clock()
        #start_text1 = 'FINAL SCORE: {}'.format(score)
        font = pg.font.SysFont('Impact', 50, False, False)
        font2 = pg.font.SysFont('Impact', 150, False, False)
        text1 = font2.render('YOU DIED', True, RED)
        textrect = text1.get_rect()
        textrect.midtop = (640, 100)
        start_text2 = 'press "Enter" to retry or "Esc" to exit'
        text2 = font.render(start_text2, True, RED)
        textrect2 = text2.get_rect()
        textrect2.midtop = (640, 390)
        start_text3 = 'You are fake news'
        text3 = font.render(start_text3, True, RED)
        textrect3 = text3.get_rect()
        textrect3.midtop = (640, 540)

        while self.playing == False:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.playing = True

            go_screen.fill(WHITE)

            go_screen.blit(text1, textrect)
            go_screen.blit(text2, textrect2)
            pg.display.flip()

            clock.tick(FPS)

    def show_win_screen(self):
        # screen when game over
        pg.init()
        go_screen = pg.display.set_mode((WIDTH, HEIGHT))
        clock = pg.time.Clock()
        # start_text1 = 'FINAL SCORE: {}'.format(score)
        font = pg.font.SysFont('Impact', 50, False, False)
        font2 = pg.font.SysFont('Impact', 150, False, False)
        text1 = font2.render('YOU WON', True, RED)
        textrect = text1.get_rect()
        textrect.midtop = (640, 100)
        start_text2 = 'press "Esc" to exit'
        text2 = font.render(start_text2, True, RED)
        textrect2 = text2.get_rect()
        textrect2.midtop = (640, 390)
        start_text3 = 'You are real news'
        text3 = font.render(start_text3, True, RED)
        textrect3 = text3.get_rect()
        textrect3.midtop = (640, 540)

        while self.playing == False:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.playing = True

            go_screen.fill(WHITE)

            go_screen.blit(text1, textrect)
            go_screen.blit(text2, textrect2)
            pg.display.flip()

            clock.tick(FPS)


##########################################################################################################
        #                               PLAY GAME                                      #
##########################################################################################################

game = Game()

game.show_start_screen()

while game.running:
    game.new()
    game.decide_screen()

pg.quit()