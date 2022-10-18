import tkinter as tk
import tkinter.messagebox as tkm


#練習3,(ボタン入力時の反応)
def click_number(event):
    btn = event.widget
    num = btn["text"]
    #tkm.showinfo(f"{num}",f"{num}のボタンが押されました")

    #練習5
    entry.insert(tk.END,num)

#練習7,=ボタン入力時の挙動
def click_equal(event):
    eqn = entry.get()
    res = eval(eqn)
    entry.delete(0,tk.END)
    entry.insert(tk.END,res)

def click_del(event):
    entry.delete(0,tk.END)

#練習1,(ウィンドウの作成)
root = tk.Tk()
root.title("不完全な電卓")
root.configure(bg="#B0C4DE")
root.geometry("290x400")

#練習4,(テキスト入力欄の追加)
entry=tk.Entry(root,width=10, font=("",40),justify="right")
entry.place(x=10,y=5)

#練習2,(数字のボタンの実装)
x,y = 10,200
numbers = list(range(9,0,-1))
for i,num in enumerate(numbers,1):
    btn = tk.Button(root,text=f"{num}",font=("",20),width=4,height=1,bg="#5f9ea0")
    btn.bind("<1>",click_number)
    btn.place(x=x, y=y)
    x += 70
    if i%3 == 0:
        y += 50
        x = 10

#0ボタンの実装
btn = tk.Button(root,text=f"0",font=("",20),width=4,height=1,bg="#5f9ea0")
btn.bind("<1>",click_number)
btn.place(x=x+70,y=y)

#小数点の実装
btn = tk.Button(root,text=f".",font=("",20),width=4,height=1)
btn.bind("<1>",click_number)
btn.place(x=x+140,y=y)

#四則演算記号の実装
mark = ["+","-","*","/"]
for m in mark:
    btn = tk.Button(root,text=f"{m}",font=("",20),width=4,height=1,bg="#AFEEEE")
    btn.bind("<1>",click_number)
    y -= 50 
    btn.place(x=x+210,y=y)

#練習7,=ボタン実装
btn = tk.Button(root,text=f"=",font=("",20),width=4,height=1,bg="#87CEEB")
btn.bind("<1>",click_equal)
btn.place(x=x+210,y=y+200)

#クリア(削除)ボタンの実装
btn = tk.Button(root,text=f"c",font=("",20),width=4,height=1,)
btn.bind("<1>",click_del)
btn.place(x=x+210,y=y-50)

root.mainloop()