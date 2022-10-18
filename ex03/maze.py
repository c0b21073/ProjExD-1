import tkinter as tk

root = tk.Tk()
root.title("迷えるこうかとん")

canvas = tk.Canvas(root, width=1500, height=900, bg='black')
canvas.pack()

tori = tk.PhotoImage(file='ex03/fig/5.png')
cx,cy = 300, 400
canvas.create_image(cx, cy, image=tori, tag='tori')

key = ""

root.mainloop()