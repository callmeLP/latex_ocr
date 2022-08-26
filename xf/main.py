import re
import pyperclip
from PIL import Image, ImageGrab,ImageTk
import os
from WebITRTeach import get_result
from tkinter import StringVar
import tkinter as tk

def start(textTemp, lab1, root_window):
    root_window.withdraw()
    os.system('RUNDLL32.EXE PrScrn.dll PrScrn')
    root_window.deiconify()
    img = ImageGrab.grabclipboard()
    if not isinstance(img, Image.Image):
        return
    print('>> 识别中...')
    image_path = "1.png"
    img.save(image_path)
    recognition = get_result()
    res = recognition.call_url(image_path)
    photo = ImageTk.PhotoImage(Image.open(image_path))
    
    os.remove(image_path)
    if res['code'] != 0:
        return
    content = res['data']['region'][0]['recog']['content']
    content = re.sub(r'ifly-latex-begin', '', content)
    content = re.sub(r'ifly-latex-end', '', content)
    content = re.sub(r'  ', '', content)
    textTemp.set(content)
    lab1.config(image = photo)
    lab1.img = photo
    # 将结果复制到剪切板
    pyperclip.copy(content)
    print(content)
 
if __name__ == '__main__':
    root_window = tk.Tk()
    root_window.attributes("-topmost",1)
    root_window.geometry("350x200")
    root_window.resizable(0, 0)
    root_window.title("img2latex")
    textTemp = StringVar()
    lab1 = tk.Label(root_window)
    button = tk.Button(root_window,text='截图',command=lambda:start(textTemp, lab1, root_window )).pack()
    lab1.pack()
    lab2 = tk.Label(root_window, textvariable = textTemp).pack()
    

    root_window.mainloop()