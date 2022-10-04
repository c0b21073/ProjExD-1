import time
import tkinter as tk


OPERATORS = ('÷', '×', '-', '+')
UES_SYMBOL = OPERATORS + ('.', '/', '//', '*', '**', '%')

def is_num(s):#入力が数値に変換できるかどうかの関数
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def check_input(s,p):
    if int(p) != 1:
        return True
    return (is_num(s) or s in UES_SYMBOL)

root = tk.Tk()
root.title('clac')
root.geometry('400x400')

check = root.register(check_input)
#entryに入力制限を設けて文字列などの
entry = tk.Entry(width=10, font=("Times New Roman",40),justify='right', validate='key', validatecommand=(check, '%S', '%d'))
entry.grid(column=0, row=0, columnspan=3)


def check_not_ope(): #直前に演算子が入力されていないかのチェック
    formula = entry.get()
    if formula: #なにか入力されていたらチェック 何も無ければFalse
        return entry.get()[-1:] not in UES_SYMBOL
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
        print(ans)
        entry.delete(0,tk.END)
        entry.insert(tk.END, str(ans))

def delete_click(event):
    entry.delete(0,tk.END)

def dotto_click(event):
    if check_not_ope():
        txt = entry.get()
        if txt[-1:] != '.':
            entry.insert(tk.END, ".")
        else:
            entry.delete(0,tk.END)
            entry.insert(tk.END, txt[:-1])

#キー入力を受付て，Enterキーでイコールとする．
def print_key(event):
    key = event.keysym
    if key == 'Return':
        equal_click(event)


entry.bind('<Key>', print_key)
entry.focus_set()


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

dotto_btn = tk.Button(root, text=".", width=4, height=2, font=('Times New Roman', 30)) # クリアボタン
dotto_btn.bind("<1>", dotto_click)
dotto_btn.grid(column=1, row=4)

root.mainloop()