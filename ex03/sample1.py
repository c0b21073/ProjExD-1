import tkinter as tk
import tkinter.messagebox as tkm

def count_up():
    global tmr
    tmr += 1
    label['text'] = tmr
    root.after(1000, count_up)

def key_down(event):
    key = event.keysym
    tkm.showinfo("キー押下", f'{key}キーが押されました')
    root.after(1000, count_up)

if __name__ == "__main__":
    root = tk.Tk()
    label = tk.Label(root, font=("", 80))
    label.pack()
    canvas = tk.Canvas(root, height=800,width=800, bg='black')
    canvas.pack()

    tori = tk.PhotoImage(file='./fig/5.png')
    cx, cy = 300,400
    canvas.create_image(cx, cy, image=tori, tag="tori")
    root.mainloop()