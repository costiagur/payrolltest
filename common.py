import tkinter
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog

replyed = 0
close = False

def intiate():
    global root
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
#

def errormsg(title,message):
    root.deiconify()
    messagebox.showerror(title=title, message=message)
    root.withdraw()
#

def infomsg(title,message):
    root.deiconify()
    messagebox.showinfo(title=title, message=message)
    root.withdraw()
#

def inputmsg(title,prompt):
    root.deiconify()
    res = simpledialog.askinteger(title=title,prompt=prompt)
    root.withdraw()
    return res
#

def pointtodir(title): #in case of direct intaraction with folders
    root.deiconify()
    res = filedialog.askdirectory(title=title)
    root.withdraw()
    return res
#

class infopopup: #to show information whithout requiring users action
    def __init__(self):
        self.top = tkinter.Toplevel(root)
        self.top.attributes("-topmost", 1)
        self.lab = tkinter.Label(self.top,text = '')
        self.lab.pack()
    #

    def show(self,newtext):
        self.lab['text'] = self.lab['text'] + "\n" + newtext
        self.lab.update()
    #        

    def close(self):
        self.top.destroy()
    #
#
