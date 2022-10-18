import tkinter as tk
from maze_maker import *

def key_down(event):
    global key
    key = event.keysym
    if key == "space":
        fly()

def key_up(event):
    global key
    key = ""

def main_proc():
    global mx, my

    if key == "Up":
        my -= 1
    elif key == "Down":
        my += 1
    elif key == "Left":
        mx -= 1
    elif key == "Right":
        mx += 1
    can_move()
    clac_c()
    canvas.coords('tori', cx, cy)
    root.after(100, main_proc)

#mx,myからcx,cyを計算する
def clac_c():
    global cx, cy
    cx = 100*mx + 50
    cy = 100*my + 50

def can_move():
    global mx,my
    if maze[my][mx] == 1 and not is_flying:
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


root = tk.Tk()
root.title("迷えるこうかとん")

canvas = tk.Canvas(root, width=1500, height=900, bg='black')
canvas.pack()

#迷路作成
maze = make_maze(15,9)
show_maze(canvas, maze)

flying_tori = tk.PhotoImage(file='ex03/fig/3.png')
tori = tk.PhotoImage(file='ex03/fig/5.png')
mx, my = 1, 1
clac_c()
canvas.create_image(cx, cy, image=tori, tag='tori')


key = ""
is_flying = False

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

main_proc()



root.mainloop()