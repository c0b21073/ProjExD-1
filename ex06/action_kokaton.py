import pygame as pg
import sys
from random import randint, choice


class Screen:
    def __init__(self, title, wh):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgs = [Background(0), Background(1500), Background(3000)]

    def blit(self, sfc, rct):
        self.sfc.blit(sfc, rct)

    def bg_update(self):
        make_bg_flag = False
        for bg in self.bgs:
            bg.rct.centerx -= move_speed
            if bg.rct.right - 100 <= 0:
                make_bg_flag = True
            self.blit(bg.sfc, bg.rct)
        if make_bg_flag:
            self.bgs.append(Background(self.bgs[-1].rct.right - 100))
            self.bgs.pop(0)


class Background:
    def __init__(self, x):
        self.sfc = pg.image.load('mt/pg_bg.jpeg')
        self.rct = self.sfc.get_rect()
        self.rct.left = x


class Bird:

    def __init__(self, file_name, x, xy):  # "mt/fig/6.png"
        self.sfc = pg.image.load(file_name)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, x)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.v0 = 0
        self.isJumping = False
        self.jumpTime = 0

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr):
        key_states = pg.key.get_pressed()
        if key_states[pg.K_SPACE]:
            self.jump()

        if self.isJumping:
            # t = (pg.time.get_ticks() - self.jumpTime) / 500
            # g = 9.8
            # y = self.v0 * t - g * (t ** 2) / 2
            self.v0 += 1
            self.rct.centery += self.v0
            if self.rct.centery > 500:
                self.rct.centery = 500
                self.isJumping = False

        self.blit(scr)  # 練習3

    def jump(self):
        if not self.isJumping:
            self.isJumping = True
            self.v0 = -27
        # self.jumpTime = pg.time.get_ticks()


class Textbook:
    def __init__(self, name, xy):
        self.sfc = pg.image.load(f'mt/textbook/{name}.png')
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.3)  # ここ倍率
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr):
        self.rct.centerx -= move_speed
        self.blit(scr)


class Books:
    def __init__(self):
        self.books = []
        self.previous_time = pg.time.get_ticks()  # ms

    def make_book(self):
        textbook_name = ('kokugo', 'eigo', 'rika', 'sugaku', 'syakai')
        now_time = pg.time.get_ticks()
        if now_time - self.previous_time > 1000:
            self.books.append(Textbook(choice(textbook_name), (1900, 500)))
            self.previous_time = now_time

    def update(self, scr, tori, clock):
        book_remove_flag = False
        for book in self.books:
            book.update(scr)
            if tori.rct.colliderect(book.rct):
                game_over(scr.sfc, clock)
                self.books = []
            if book.rct.right < 0:
                book_remove_flag = True
        if book_remove_flag:
            self.books.pop(0)


def game_over(sfc, clock):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                return
        # ゲームオーバーの文字表示
        afonto = pg.font.Font(None, 80)
        atxt = afonto.render("GAME OVER", True, (0, 0, 0))
        arct = atxt.get_rect()
        arct.center = 800, 450
        sfc.blit(atxt, arct)
        bfonto = pg.font.Font(None, 50)
        btxt = bfonto.render("press 'R' to restart", True, (0, 0, 0))
        brct = btxt.get_rect()
        brct.center = 800, 550
        sfc.blit(btxt, brct)

        pg.display.update()
        clock.tick(1000)


def main():
    scr = Screen('アクションこうかとん', (1700, 900))
    tori = Bird("mt/fig/3_reverse.png", 2.5, (180, 500))
    books = Books()
    clock = pg.time.Clock()

    while True:
        scr.bg_update()
        tori.update(scr)
        if randint(0, 100) == 98:
            books.make_book()
        books.update(scr, tori, clock)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()  # 練習2
        clock.tick(1000)


if __name__ == "__main__":
    move_speed = 9
    pg.init()
    main()
    pg.quit()
    sys.exit()
