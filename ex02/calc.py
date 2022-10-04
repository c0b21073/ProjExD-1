import tkinter as tk
import tkinter.messagebox as tkm
from turtle import right

OPERATORS = ('÷', '×', '-', '+')

root = tk.Tk()
root.title('clac')
root.geometry('400x400')

entry = tk.Entry(width=10, font=("Times New Roman",40),justify='right')
entry.grid(column=0, row=0, columnspan=3)

def check_not_ope(): #直前に演算子が入力されていないかのチェック
    formula = entry.get()
    if formula: #なにか入力されていたらチェック 何も無ければFalse
        return entry.get()[-1:] not in OPERATORS
    return False


def num_click(event):
    btn = event.widget
    txt = btn["text"]
    entry.insert(tk.END, txt)

def ope_click(event):
    if check_not_ope():
        btn = event.widget
        txt = btn["text"]
        entry.insert(tk.END, txt)

def equal_click(event):
    if check_not_ope():
        formula = entry.get().replace('×', '*').replace('÷', '/')#演算子をPython仕様に置き換え
        ans = eval(formula)
        entry.delete(0,tk.END)
        entry.insert(tk.END, str(ans))

def delete_click(event):
    entry.delete(0,tk.END)

for i in range(9, -1, -1):#数字の配置
    index = 9 - i #場所指定のためのindex
    button = tk.Button(root, text=str(i),width=4, height=2, font=('Times New Roman', 30))
    button.bind("<1>", num_click)
    button.grid(column=index%3, row=(index//3) + 1)

for j, operator in enumerate(OPERATORS):#演算子の配置
    ope_btn = tk.Button(root, text=operator, width=4, height=2, font=('Times New Roman', 30))
    ope_btn.bind("<1>", ope_click)
    ope_btn.grid(column=3, row=j+1)

equal_btn = tk.Button(root, text="=", width=4, height=2, font=('Times New Roman', 30))
equal_btn.bind("<1>", equal_click)
equal_btn.grid(column=2, row=4)

delete_btn = tk.Button(root, text="c", width=4, height=2, font=('Times New Roman', 30)) # クリアボタン
delete_btn.bind("<1>", delete_click)
delete_btn.grid(column=3, row=0)

root.mainloop()