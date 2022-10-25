import pygame as pg
import sys

def make_img(path, x, y, r=0, m=1.0):
    sfc = pg.image.load(path)
    sfc = pg.transform.rotozoom(sfc, r, m)
    rct = sfc.get_rect()
    rct.center = x, y
    return sfc, rct

def main():
    pg.display.set_caption("逃げろ!こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    back_sfc = pg.image.load('mt/pg_bg.jpeg')
    clock = pg.time.Clock()
    tori_sfc, tori_rct = make_img("mt/fig/6.png", 900,400, m=2.0)

    while True:
        scrn_sfc.blit(back_sfc, (0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        key_list = pg.key.get_pressed()
        if key_list[pg.K_UP]:
            tori_rct.centery -= 1
        if key_list[pg.K_DOWN]:
            tori_rct.centery += 1
        if key_list[pg.K_RIGHT]:
            tori_rct.centerx += 1
        if key_list[pg.K_LEFT]:
            tori_rct.centerx -= 1

        scrn_sfc.blit(tori_sfc, tori_rct)
        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()