import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk()
root.title('clac')
root.geometry('300x500')

for i in range(9, -1, -1):
    index = 9 - i
    button = tk.Button(root, text=str(i),width=4, height=2, font=('Times New Roman', 30))
    button.grid(column=index%3, row=index//3)

root.mainloop()