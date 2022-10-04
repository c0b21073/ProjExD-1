import tkinter as tk
import tkinter.messagebox as tkm
from turtle import right

OPERATORS = ('+', '-', '×', '÷')

root = tk.Tk()
root.title('clac')
root.geometry('300x400')

entry = tk.Entry(width=10, font=("Times New Roman",40),justify='right')
entry.grid(column=0, row=0, columnspan=3)

def check_not_ope(): #直前に演算子が入力されていないかのチェック
    formula = entry.get()
    if formula:
        return entry.get()[-1:] not in OPERATORS
    return False


def num_click(event):
    btn = event.widget
    txt = btn["text"]
    entry.insert(tk.END, txt)

def plus_click(event):
    if check_not_ope():
        entry.insert(tk.END, "+")

def equal_click(event):
    if check_not_ope():
        formula = entry.get()
        ans = eval(formula)
        entry.delete(0,tk.END)
        entry.insert(tk.END, str(ans))

for i in range(9, -1, -1):
    index = 9 - i #場所指定のためのindex
    button = tk.Button(root, text=str(i),width=4, height=2, font=('Times New Roman', 30))
    button.bind("<1>", num_click)
    button.grid(column=index%3, row=(index//3) + 1)

plus_btn = tk.Button(root, text="+", width=4, height=2, font=('Times New Roman', 30))
plus_btn.bind("<1>", plus_click)
plus_btn.grid(column=1, row=4)

equal_btn =  tk.Button(root, text="=", width=4, height=2, font=('Times New Roman', 30))
equal_btn.bind("<1>", equal_click)
equal_btn.grid(column=2, row=4)


root.mainloop()