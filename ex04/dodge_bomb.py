from cgitb import reset
import pygame as pg
import sys
from random import randint

#画像配置
def make_img(path, x, y, r=0, m=1.0):
    sfc = pg.image.load(path)
    sfc = pg.transform.rotozoom(sfc, r, m)
    rct = sfc.get_rect()
    rct.center = x, y
    return sfc, rct

#爆弾生成
def make_bomb(tori_rct):
    sfc = pg.Surface((20,20))
    pg.draw.circle(sfc,(255,0,0),(10,10), 10)
    sfc.set_colorkey('black')
    rct = sfc.get_rect()
    #爆弾生成時にこうかとんとかぶって生成されないように調整
    while True:
        bomb_x, bomb_y = randint(10,1590), randint(10, 890)
        rct.center = bomb_x,bomb_y
        if not rct.colliderect(tori_rct):
            break
    return sfc, rct

#ゲームオーバー処理
def game_over(sfc, clock):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                return
        #ゲームオーバーの文字表示
        afonto = pg.font.Font(None, 80)
        atxt = afonto.render("GAME OVER", True, (0,0,0))
        arct = atxt.get_rect()
        arct.center = 800, 450
        sfc.blit(atxt, arct)
        bfonto = pg.font.Font(None, 50)
        btxt = bfonto.render("press 'R' to restart", True, (0,0,0))
        brct = btxt.get_rect()
        brct.center = 800, 550
        sfc.blit(btxt, brct)

        pg.display.update()
        clock.tick(1000)
        


def main():
    pg.display.set_caption("逃げろ!こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    back_sfc = pg.image.load('mt/pg_bg.jpeg')
    clock = pg.time.Clock()
    tori_sfc, tori_rct = make_img("mt/fig/6.png", 900,400, m=2.0)
    vx, vy = 1, 1
    bomb_sfc, bomb_rct = make_bomb(tori_rct)


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
        
        scrn_sfc.blit(bomb_sfc, bomb_rct)
        if not 10 <= bomb_rct.centerx <= 1590:
            vx *= -1
        if not 10 <= bomb_rct.centery <= 890:
            vy *= -1
        bomb_rct = bomb_rct.move(vx,vy)

        
        pg.display.update()
        if tori_rct.colliderect(bomb_rct):
            game_over(scrn_sfc,clock)
            vx, vy = 1, 1
            bomb_sfc, bomb_rct = make_bomb(tori_rct)
            
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()