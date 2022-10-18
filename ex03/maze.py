import tkinter as tk
from maze_maker import *

def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy
    if key == "Up":
        cy -= 20
    elif key == "Down":
        cy += 20
    elif key == "Left":
        cx -= 20
    elif key == "Right":
        cx += 20
    canvas.coords('tori', cx, cy)
    root.after(100, main_proc)

    
    

root = tk.Tk()
root.title("迷えるこうかとん")

canvas = tk.Canvas(root, width=1500, height=900, bg='black')
canvas.pack()

#迷路作成
maze = make_maze(15,9)
show_maze(canvas, maze)

tori = tk.PhotoImage(file='ex03/fig/5.png')
cx,cy = 300, 400
canvas.create_image(cx, cy, image=tori, tag='tori')

key = ""

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

main_proc()



root.mainloop()