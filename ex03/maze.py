from cgitb import reset
import tkinter as tk
from maze_maker import *

def key_down(event):
    global key
    key = event.keysym
    if key == "space":
        fly()
    if key == 'r':
        reset()

def key_up(event):
    global key
    key = ""

def main_proc():
    global mx, my, cx, cy

    if key == "Up":
        my -= 1
    elif key == "Down":
        my += 1
    elif key == "Left":
        mx -= 1
    elif key == "Right":
        mx += 1
    can_move()
    cx,cy = clac_c(mx, my)
    canvas.coords('tori', cx, cy)
    is_goal()
    root.after(100, main_proc)

#mx,myからcx,cyを計算する
def clac_c(x,y):
    return 100*x + 50, 100*y + 50

#動けなかったらmx,myを戻す
def can_move():
    global mx,my
    if (not(is_flying or maze[my][mx] == 0)) or not can_mo:
        if key == "Up":
            my += 1
        elif key == "Down":
            my -= 1
        elif key == "Left":
            mx += 1
        elif key == "Right":
            mx -= 1


def fly():
    global is_flying
    canvas.delete('tori')
    if is_flying:
        is_flying = False
        canvas.create_image(cx, cy, image=tori, tag='tori')
    else:
        is_flying = True
        canvas.create_image(cx, cy, image=flying_tori, tag='tori')

#スタートから一番遠い行き止まりをゴールとする．
def make_goal():
    end_list = []
    #行き止まり判定
    for i in range(tate)[1:-1]:
        for j in range(yoko)[1:-1]:
            up = maze[j-1][i]
            down = maze[j+1][i]
            left = maze[j][i-1]
            right = maze[j][i+1]
            sum_ = up + down + left + right
            if sum_ >= 3 and maze[j][i] == 0:
                end_list.append((j,i))
    #一番遠いマスを返す
    end_list.sort(key=lambda x: x[0]+x[1])
    return end_list[-1]
            
def is_goal():
    global can_mo
    if goal == (my, mx):
        can_mo = False
        canvas.delete('tori')
        canvas.create_image(cx, cy, image=goal_tori, tag='tori')
        label = tk.Label(root, text='GOAL',font=('', 100))
        label.pack()
            
def reset():
    pass


key = ""
is_flying = False
can_mo = True


root = tk.Tk()
root.title("迷えるこうかとん")

canvas = tk.Canvas(root, width=1500, height=900, bg='black')
canvas.pack()

tate = 15
yoko = 9
#迷路作成
maze = make_maze(tate,yoko)
show_maze(canvas, maze)
canvas.create_rectangle(100, 100,200, 200, fill='red')
goal = make_goal()
goal_m = clac_c(goal[0], goal[1])
canvas.create_rectangle(goal_m[1]-50, goal_m[0]-50,goal_m[1]+50, goal_m[0]+50, fill='blue')

flying_tori = tk.PhotoImage(file='ex03/fig/3.png')
tori = tk.PhotoImage(file='ex03/fig/5.png')
goal_tori = tk.PhotoImage(file='ex03/fig/6.png')
mx, my = 1, 1
cx, cy = clac_c(mx,my)
canvas.create_image(cx, cy, image=tori, tag='tori')


key = ""
is_flying = False
can_mo = True

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

main_proc()

root.mainloop()