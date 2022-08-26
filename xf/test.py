from tkinter import *  
from tkinter.filedialog import askopenfilename  
from PIL import Image,ImageTk 
  
def choosepic():  
    path_=askopenfilename()  
    path.set(path_)  
    img_open = Image.open(e1.get())  
    img=ImageTk.PhotoImage(img_open)  
    l1.config(image=img)  
    l1.image=img #keep a reference  
      
root=Tk()  
path=StringVar()  
Button(root,text='选择图片',command=choosepic).pack()  
e1=Entry(root,state='readonly',text=path)  
e1.pack()  
l1=Label(root)  
l1.pack()  
root.mainloop()