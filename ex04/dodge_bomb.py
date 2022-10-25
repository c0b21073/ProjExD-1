import pygame as pg
import sys

def make_img(main_sfc, path, x, y, r=0, m=1.0):
    sfc = pg.image.load(path)
    sfc = pg.transform.rotozoom(sfc, r, m)
    rct = sfc.get_rect()
    rct.center = x, y
    main_sfc.blit(sfc, rct)

def main():
    pg.display.set_caption("逃げろ!こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    back_sfc = pg.image.load('mt/pg_bg.jpeg')
    clock = pg.time.Clock()
    scrn_sfc.blit(back_sfc, (0,0))
    make_img(scrn_sfc, "mt/fig/6.png", 900,400, m=2.0)


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()