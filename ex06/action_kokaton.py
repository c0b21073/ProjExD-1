import pygame as pg
import sys
from random import randint, choice


class Screen:
    def __init__(self, title, wh):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgs = [Background(0), Background(1500), Background(3000)]  # 背景を動かすので3枚生成

    def blit(self, sfc, rct):
        self.sfc.blit(sfc, rct)

    # 背景を動かし，追加したり削除したり
    def bg_update(self):
        make_bg_flag = False
        for bg in self.bgs:
            bg.rct.centerx -= move_speed
            if bg.rct.right - 100 <= 0:
                make_bg_flag = True
            self.blit(bg.sfc, bg.rct)
        if make_bg_flag:  # 画面外の背景を削除し，新たに右に背景を生成する
            self.bgs.append(Background(self.bgs[-1].rct.right - 100))  # 一番見栄えがいい設定
            self.bgs.pop(0)


# 背景クラス
class Background:
    def __init__(self, x):
        self.sfc = pg.image.load('mt/pg_bg.jpeg')
        self.rct = self.sfc.get_rect()
        self.rct.left = x


# スコアクラス
class Score:
    def __init__(self):
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.font = pg.font.Font(None, 50)

    def update(self, scr):  # スコアは経過時間と飛び越えた本の数で決定される
        time = pg.time.get_ticks() - self.start_time
        score = int(time // 100)
        txt = self.font.render(f'score : {score + (num_of_books * 10)}', True, (0, 0, 0))
        scr.blit(txt, (0, 0))


# 体力を表すハートのオブジェクト
class Heart:
    def __init__(self, xy):
        self.sfc = pg.image.load('mt/heart.png')
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.1)  # ここ倍率
        self.rct = self.sfc.get_rect()
        self.rct.center = xy


# 体力をまとめて管理するオブジェクト
class Hearts:
    def __init__(self):
        # 3つ生成
        self.hearts = [Heart((1450, 50)), Heart((1500, 50)), Heart((1550, 50))]
        self.previous_time = 0

    def __len__(self):
        return len(self.hearts)

    def reset(self):  # ハートを生成し直す(リスタート時)
        self.__init__()

    def damage(self, scr):  # ダメージを負ったときの処理
        time = pg.time.get_ticks()
        if time - self.previous_time > 700:  # 連続して当たらないように無敵時間設定
            self.hearts.pop(0)
            self.update(scr)
            self.previous_time = time

    def update(self, scr):
        for heart in self.hearts:
            scr.blit(heart.sfc, heart.rct)


# プレイヤークラス
class Bird:

    def __init__(self, file_name, x, xy):  # "mt/fig/6.png"
        self.sfc = pg.image.load(file_name)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, x)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.v0 = 0  # ジャンプ力
        self.isJumping = False  # ジャンプしてるかどうか

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr):
        key_states = pg.key.get_pressed()
        if key_states[pg.K_SPACE]:  # SPACEキーを押したらジャンプ
            self.jump()

        if self.isJumping:
            self.v0 += 1  # ジャンプしてるなら上への力を少しへらす
            self.rct.centery += self.v0
            if self.rct.centery > 500:  # 基準(地面)より下に行ったらジャンプ終了＆基準に修正
                self.rct.centery = 500
                self.isJumping = False

        self.blit(scr)

    def jump(self):  # ジャンプメソット
        if not self.isJumping:  # ジャンプ中にはジャンプしない
            self.isJumping = True
            self.v0 = -27  # ジャンプ力（上への力）


# 本1冊のクラス
class Textbook:
    def __init__(self, name, xy):
        self.sfc = pg.image.load(f'mt/textbook/{name}.png')
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.3)  # ここ倍率
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr):
        scr.blit(self.sfc, self.rct)

    def update(self, scr):  # 本を動かす
        self.rct.centerx -= move_speed
        self.blit(scr)


# 本をまとめて管理するクラス
class Books:
    def __init__(self):
        self.books = []
        self.previous_time = pg.time.get_ticks()  # ms

    def make_book(self):
        textbook_name = ('kokugo', 'eigo', 'rika', 'sugaku', 'syakai')  # 生成される教科書の種類(ランダム)
        now_time = pg.time.get_ticks()
        if now_time - self.previous_time > 1000:  # 連続して本が生成されないように配慮
            self.books.append(Textbook(choice(textbook_name), (1900, 500)))  # ランダムな教科書生成
            self.previous_time = now_time

    def update(self, scr, tori, clock, score, hearts):
        global num_of_books
        book_remove_flag = False
        for book in self.books:  # 本を一冊づつ動かす
            book.update(scr)
            # プレイヤーと本がぶつかっていないか確認＆ゲームオーバーなら初期化
            if tori.rct.colliderect(book.rct):
                hearts.damage(scr)
                if len(hearts) <= 0:
                    game_over(scr.sfc, clock)  # ゲームオーバー関数，以下初期化
                    self.books = []
                    score.start_time = pg.time.get_ticks()
                    num_of_books = 0
                    hearts.reset()
            if book.rct.right < 0:  # 画面外に本が出たら消す
                book_remove_flag = True
        # 画面外の本を消す処理
        if book_remove_flag:
            self.books.pop(0)
            num_of_books += 1


# ゲームオーバー処理
def game_over(sfc, clock):
    # ゲームオーバー画面への遷移
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # 'R'キーを押したらリスタート
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
    scr = Screen('アクションこうかとん', (1600, 900))
    tori = Bird("mt/fig/3_reverse.png", 2.5, (180, 500))
    books = Books()
    clock = pg.time.Clock()
    score = Score()
    hearts = Hearts()

    # メインループ
    while True:
        scr.bg_update()
        tori.update(scr)
        # 本が生成される条件
        if randint(0, 100) == 98:
            books.make_book()
        books.update(scr, tori, clock, score, hearts)
        score.update(scr)
        hearts.update(scr)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    move_speed = 9  # オブジェクトが進むスピード
    num_of_books = 0  # 飛び越えた本の数(スコアの計算に利用)
    pg.init()
    main()
    pg.quit()
    sys.exit()
