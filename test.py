import pygame as pg
import sys

def main():
    pg.display.set_caption("初めてのPython")
    scrn_sfc = pg.display.set_mode((800,600))
    tori_sfc = pg.image.load('mt/fig/6.png')
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 700, 400
    scrn_sfc.blit(tori_sfc, tori_rct)

    fonto = pg.font.Font(None, 80)
    txt = fonto.render(str(tmr), True, WHITE)
    while True:
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()