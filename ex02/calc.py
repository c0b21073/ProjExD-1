import tkinter as tk
import tkinter.messagebox as tkm
from turtle import right

root = tk.Tk()
root.title('clac')
root.geometry('300x400')

def num_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt, f'{txt}のボタンがクリックされました')

entry = tk.Entry(width=10, font=("Times New Roman",40),justify='right')
entry.grid(column=0, row=0, columnspan=3)

for i in range(9, -1, -1):
    index = 9 - i #場所指定のためのindex
    button = tk.Button(root, text=str(i),width=4, height=2, font=('Times New Roman', 30))
    button.bind("<1>", num_click)
    button.grid(column=index%3, row=(index//3) + 1)

root.mainloop()