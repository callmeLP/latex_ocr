import tkinter as tk
from PIL import ImageTk
from PIL import Image as imim
from tkinter import  messagebox

root_window = tk.Tk()
root_window.geometry("450x300")
root_window.resizable(0, 0)
root_window.title("img2latex")

photo = ImageTk.PhotoImage(imim.open("test.png"))

def click_button():
    messagebox.showinfo(title='温馨提示', message='欢迎使用C语言中文网')

lab1 = tk.Label(root_window, image = photo).pack()
lab2 = tk.Label(root_window, text= "").pack()
button = tk.Button(root_window,text='点击前往',bg='#7CCD7C',command=click_button).pack()

root_window.mainloop()