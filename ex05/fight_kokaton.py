import pygame as pg
import sys
from random import randint

key_delta = {
    pg.K_UP: [0, -1],
    pg.K_DOWN: [0, +1],
    pg.K_LEFT: [-1, 0],
    pg.K_RIGHT: [+1, 0],
}


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
        pg.K_UP: [0, -1],
        pg.K_DOWN: [0, +1],
        pg.K_LEFT: [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, file_name, x, xy):  # "mt/fig/6.png"
        self.sfc = pg.image.load(file_name)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, x)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr):
        key_states = pg.key.get_pressed()
        for key, delta in key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                # 練習7
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.blit(scr)  # 練習3


class Bomb:
    def __init__(self, color, r, speed_t, scr):
        self.sfc = pg.Surface((r * 2, r * 2))  # 空のSurface
        self.sfc.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (r, r), r)  # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = speed_t

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr):
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.rct.move_ip(self.vx, self.vy)  # 練習6
        scr.blit(self.sfc, self.rct)  # 練習5


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


def main():
    # 練習1
    scr = Screen('逃げろこうかとん!', (1600, 900), 'mt/pg_bg.jpeg')
    # 練習3
    tori = Bird("mt/fig/6.png", 2, (900, 600))

    # 練習5
    bomb = Bomb((255, 0, 0), 10, (1, 1), scr)

    clock = pg.time.Clock()  # 練習1
    while True:
        scr.blit(scr.bg_sfc, scr.bg_rct)  # 練習2

        for event in pg.event.get():  # 練習2
            if event.type == pg.QUIT:
                return

        tori.update(scr)

        # 練習7
        bomb.update(scr)

        # 練習8
        if tori.rct.colliderect(bomb.rct):  # こうかとんrctが爆弾rctと重なったら
            return

        pg.display.update()  # 練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()  # 初期化
    main()  # ゲームの本体
    pg.quit()  # 初期化の解除
    sys.exit()
