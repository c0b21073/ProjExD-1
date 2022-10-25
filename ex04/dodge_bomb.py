from cgitb import reset
from secrets import choice
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
    return [sfc, rct]

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
        
#スコア計算＆表示
def show_score(sfc, num):
    time = pg.time.get_ticks() - previaus_time
    fonto = pg.font.Font(None, 50)
    score = int(time//100)
    txt = fonto.render(f'score : {score+(num*50)}', True, (0,0,0))
    sfc.blit(txt, (0,0))
    return score

#りんご作成
def make_apple(main_sfc, sfc, rct, half):
    global app_flag, app_x, app_y
    if app_flag:
        app_x, app_y = randint(0+half, 1600-half), randint(0+half, 900-half)
        app_flag = False
        rct.center = app_x, app_y
    main_sfc.blit(sfc, rct)
    return rct



def main():
    global app_flag
    pg.display.set_caption("逃げろ!こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    back_sfc = pg.image.load('mt/pg_bg.jpeg')
    clock = pg.time.Clock()
    tori_sfc, tori_rct = make_img("mt/fig/6.png", 900,400, m=2.0)
    bomb_v = []
    bomb_list = []
    #爆弾の個数
    bomb_num = 5
    #爆弾を複数個生成
    for i in range(bomb_num):
        bomb_list.append(make_bomb(tori_rct))
        bomb_v.append([choice([-1,1]),choice([-1,1])])
    
    previaus_score = 0

    #りんごの設定
    app_sfc, app_rct = make_img("mt/fruit_apple.png", 300,300, m=0.2)
    app_half = app_rct.width//2
    app_num = 0

    tori_speed = 1
    

    #メインループ
    while True:
        scrn_sfc.blit(back_sfc, (0,0))
        #りんご生成
        app_rct = make_apple(scrn_sfc, app_sfc, app_rct, app_half)
        
        #りんご取得判定
        if tori_rct.colliderect(app_rct):
            app_num += 1 
            app_flag = True


        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        #移動
        key_list = pg.key.get_pressed()
        if key_list[pg.K_UP]: 
            if 0 < tori_rct.top: 
                tori_rct.centery -= tori_speed
        if key_list[pg.K_DOWN]: 
            if tori_rct.bottom < 900:
                tori_rct.centery += tori_speed
        if key_list[pg.K_RIGHT]: 
            if tori_rct.right < 1600:
                tori_rct.centerx += tori_speed
        if key_list[pg.K_LEFT]: 
            if 0 < tori_rct.left:
                tori_rct.centerx -= tori_speed

        scrn_sfc.blit(tori_sfc, tori_rct)
        
        #全爆弾を動かす
        for i, v in zip(bomb_list, bomb_v):
            scrn_sfc.blit(i[0], i[1])
            if not 10 <= i[1].centerx <= 1590:
                v[0] *= -1
            if not 10 <= i[1].centery <= 890:
                v[1] *= -1
            i[1] = i[1].move(v[0],v[1])

        #時間が経つと2倍に
        score = show_score(scrn_sfc, app_num)
        if score - previaus_score > 100:
            for n in bomb_v:
                n[0] *= 2
                n[1] *= 2
            tori_speed *= 2
            previaus_score = score
       
        pg.display.update()
        #全爆弾のゲームオーバー判定
        for j in bomb_list:
            if tori_rct.colliderect(j[1]):
                #ゲームオーバー処理
                game_over(scrn_sfc,clock)
                bomb_v = []
                bomb_list = []
                for i in range(bomb_num):
                    bomb_list.append(make_bomb(tori_rct))
                    bomb_v.append([choice([-1,1]),choice([-1,1])])
                global previaus_time
                previaus_time = pg.time.get_ticks()
                previaus_score = 0
                app_flag = True
                app_num = 0
                tori_speed = 1

        clock.tick(1000)

if __name__ == "__main__":
    previaus_time = 0.0
    app_flag = True
    app_x, app_y = 0,0
    pg.init()
    main()
    pg.quit()
    sys.exit()