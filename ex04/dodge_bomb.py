import pygame as pg
import sys
from random import randint

def make_img(path, x, y, r=0, m=1.0):
    sfc = pg.image.load(path)
    sfc = pg.transform.rotozoom(sfc, r, m)
    rct = sfc.get_rect()
    rct.center = x, y
    return sfc, rct

def make_bomb():
    sfc = pg.Surface((20,20))
    pg.draw.circle(sfc,(255,0,0),(10,10), 10)
    sfc.set_colorkey('black')
    return sfc


def main():
    pg.display.set_caption("逃げろ!こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    back_sfc = pg.image.load('mt/pg_bg.jpeg')
    clock = pg.time.Clock()
    tori_sfc, tori_rct = make_img("mt/fig/6.png", 900,400, m=2.0)
    bomb_x, bomb_y = randint(10,1590), randint(10, 890)
    vx, vy = 1, 1


    while True:
        scrn_sfc.blit(back_sfc, (0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        key_list = pg.key.get_pressed()
        if key_list[pg.K_UP]: 
            if 0 < tori_rct.top: 
                tori_rct.centery -= 1
        if key_list[pg.K_DOWN]: 
            if tori_rct.bottom < 900:
                tori_rct.centery += 1
        if key_list[pg.K_RIGHT]: 
            if tori_rct.right < 1600:
                tori_rct.centerx += 1
        if key_list[pg.K_LEFT]: 
            if 0 < tori_rct.left:
                tori_rct.centerx -= 1

        scrn_sfc.blit(tori_sfc, tori_rct)
        scrn_sfc.blit(make_bomb(), (bomb_x,bomb_y))
        if not 10 <= bomb_x <= 1590:
            vx *= -1
        bomb_x += vx
        if not 10 <= bomb_y <= 890:
            vy *= -1
        bomb_y += vy

        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()