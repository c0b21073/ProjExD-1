import pygame as pg
import sys
from random import randint
from random import choice

def make_img(path, x, y, r=0, m=1.0):
    sfc = pg.image.load(path)
    sfc = pg.transform.rotozoom(sfc, r, m)
    rct = sfc.get_rect()
    rct.center = x, y
    return sfc, rct
def make_apple(main_sfc, sfc, rct, half):
    global app_flag, app_x, app_y
    if app_flag:
        app_x, app_y = randint(0+half, 1600-half), randint(0+half, 900-half)
        app_flag = False
        rct.center = app_x, app_y
    main_sfc.blit(sfc, rct)
    return rct
class Screen:
    def __init__(self, title, wh, bg_img):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bg_sfc = pg.image.load(bg_img)
        self.bg_rct = self.bg_sfc.get_rect()

    def blit(self, sfc, rct):
        self.sfc.blit(sfc, rct)


class Bird:
    key_delta = {
        pg.K_UP: [0, -3],
        pg.K_DOWN: [0, +3],
        pg.K_LEFT: [-3, 0],
        pg.K_RIGHT: [+3, 0],
    }

    def __init__(self, file_name, x, xy):  # "mt/fig/6.png"
        self.sfc = pg.image.load(file_name)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, x)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.baletts = []
        self.x = 0
        self.y = 0

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr, yokai):
        key_states = pg.key.get_pressed()
        for key, delta in self.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.x = delta[0]+2
                self.rct.centery += delta[1]
                self.y = delta[1]+2
                # 練習7
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        for balett in self.baletts:
            balett.update(scr, yokai.rct)
        if key_states[pg.K_SPACE]:
            self.make_balett()
        self.blit(scr)  # 練習3

    def make_balett(self):
        ballet = Balett((0, 0, 255), 10, (-2, 0),  self.rct.center)
        self.baletts.append(ballet)

class Bomb:
    def __init__(self, color, r, speed_t, scr, xy):
        self.sfc = pg.Surface((r * 2, r * 2))  # 空のSurface
        self.sfc.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (r, r), r)  # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = xy[0]
        self.rct.centery = xy[1]
        self.vx, self.vy = speed_t

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr, tori_rct):
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.rct.move_ip(self.vx, self.vy)  # 練習6
        scr.blit(self.sfc, self.rct)  # 練習5
        if tori_rct.colliderect(self.rct):
            game_over(scr)


class Yokai:
    def __init__(self, file_name, x, xy, hp):
        self.sfc = pg.image.load(file_name)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, x)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.hp = hp
        self.bombs = []

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr, player_rct):
        self.x = (player_rct.centerx - self.rct.centerx)
        self.y = (player_rct.centery - self.rct.centery)
        self.vx, self.vy = (self.x/self.y),(self.y/self.x)
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        if yoko == -1:
            self.vx *= yoko * 2
            self.rct.move_ip(self.vx, 0)
        if tate == -1:
            self.vy *= tate * 2
            self.rct.move_ip(0, self.vy)
        self.blit(scr.sfc)
        for bom in self.bombs:
            bom.update(scr, player_rct)
        if randint(1,100) < 3:
            self.make_bomb(scr)

    def make_bomb(self, scr):
        bomb = Bomb((255, 0, 0), 10, (randint(-2,2), randint(-2,2)), scr, self.rct.center)
        self.bombs.append(bomb)

    def remove_bomb(self):
        self.bombs = []

class Balett:
    def __init__(self, color, r, speed_t, xy):
        self.sfc = pg.Surface((r * 2, r * 2))  # 空のSurface
        self.sfc.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (r, r), r)  # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = xy[0]
        self.rct.centery = xy[1]
        self.vx, self.vy = speed_t

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr, yokai):

        self.rct.move_ip(self.vx, self.vy)  # 練習6
        scr.blit(self.sfc, self.rct)  # 練習5
        if yokai.colliderect(self.rct):
            clear(scr.sfc)

def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

def clear(sfc):
    clock = pg.time.Clock()  # 練習1
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                main()
        #ゲームオーバーの文字表示
        afonto = pg.font.Font(None, 80)
        atxt = afonto.render("ClEAR!", True, (122,122,255))
        arct = atxt.get_rect()
        arct.center = 800, 450
        sfc.blit(atxt, arct)
        bfonto = pg.font.Font(None, 50)
        btxt = bfonto.render("press 'R' to restart", True, (122,122,255))
        brct = btxt.get_rect()
        brct.center = 800, 550
        sfc.blit(btxt, brct)
        pg.display.update()
        clock.tick(1000)

def game_over(sfc):
    clock = pg.time.Clock()  # 練習1

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                main()
        #ゲームオーバーの文字表示
        afonto = pg.font.Font(None, 80)
        atxt = afonto.render("GAME OVER", True, (122,122,255))
        arct = atxt.get_rect()
        arct.center = 800, 450
        sfc.blit(atxt, arct)
        bfonto = pg.font.Font(None, 50)
        btxt = bfonto.render("press 'R' to restart", True, (122,122,255))
        brct = btxt.get_rect()
        brct.center = 800, 550
        sfc.blit(btxt, brct)
        pg.display.update()
        clock.tick(1000)
def main():
    # 練習1
    scr = Screen('逃げろこうかとん!', (1600, 900), 'mt/pg_bg.jpeg')
    # 練習3
    tori = Bird("mt/fig/6.png", 2, (900, 600))

    # 練習5

    yokai = Yokai('mt/youkai.png', 0.5, (500, 400), 100)
    app_sfc, app_rct = make_img("mt/fruit_apple.png", 300, 300, m=0.2)
    app_half = app_rct.width // 2

    clock = pg.time.Clock()  # 練習1
    while True:
        scr.blit(scr.bg_sfc, scr.bg_rct)  # 練習2

        for event in pg.event.get():  # 練習2
            if event.type == pg.QUIT:
                pg.quit()  # 初期化の解除
                sys.exit()
        app_rct = make_apple(scr.sfc, app_sfc, app_rct, app_half)

        # りんご取得判定
        if tori.rct.colliderect(app_rct):
            yokai.remove_bomb()
        tori.update(scr, yokai)

        # 練習7

        yokai.update(scr, tori.rct)


        # 練習8
        if tori.rct.colliderect(yokai.rct):  # こうかとんrctが爆弾rctと重なったら
            game_over(scr.sfc)

        pg.display.update()  # 練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()  # 初期化
    app_flag = True
    main()  # ゲームの本体
    pg.quit()  # 初期化の解除
    sys.exit()
