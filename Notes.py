
import tkinter as tk
import markdown2
from tkhtmlview import HTMLLabel
import ctypes
from PIL import Image,ImageTk

class NoteSystem(object):
    def __init__(self):
        self.showMode = "alwaysTop"
        self.onEdit = False
        
        self.icoPath = "icon"
        self.root = tk.Tk()
        self.root.title("便签")
        self.root.iconbitmap(self.icoPath+r"\icon.ico")
        self.root.resizable(True, True) 
        self.afterId = 336436840
        self.root.geometry("%dx%d"%(500,300))
        self.root.geometry("+%d+%d"%(abs(self.root.winfo_screenwidth()-500),500))#好像没用
        self.root.wm_attributes('-topmost',1)
        self.root.wm_attributes('-toolwindow',1)
        self.editBox = tk.Text(self.root,undo=True,font=("等线",14))
        self.savedBox = HTMLLabel(self.root,background="white",html="",font=("等线",14))
        self.saveIco = ImageTk.PhotoImage(Image.open(self.icoPath+r"\save.png"))
        self.editIco = ImageTk.PhotoImage(Image.open(self.icoPath+r"\edit.png"))
        self.alwaysTopIco = ImageTk.PhotoImage(Image.open(self.icoPath+r"\alwaysTop.png"))
        self.onDesktopIco = ImageTk.PhotoImage(Image.open(self.icoPath+r"\onDesktop.png"))
        self.minimizedIco = ImageTk.PhotoImage(Image.open(self.icoPath+r"\minimized.png"))
        self.button = tk.Button(self.root,command=self.save_edit,bg="white",relief="flat")
        self.button.place(relx=1,rely=1,x=-30,y=-30)
        self.button2 = tk.Button(self.root,image=self.onDesktopIco,command=self.change_show_mode,bg="white",relief="flat")
        self.button2.place(relx=1,rely=1,x=-70,y=-30)
        self.button3 = tk.Button(self.root,image=self.minimizedIco,command=self.minimize,bg="white",relief="flat")
        self.button3.place(relx=1,rely=1,x=-100,y=-30)
        self.editBox.bind("<Control-z>",self.undo)
        self.editBox.bind("<Control-y>",self.redo)
        self.save_edit()
        self.loadNote()
        self.loop()
        self.root.mainloop()
    
    def undo(self,event):
        self.editBox.edit_undo()
    def redo(self,event):
        self.editBox.edit_redo()
    def saveNote(self):
        with open("note.txt",'w',errors='ignore') as f:
            f.write(self.editBox.get("1.0","end"))
    def loadNote(self):
        with open("note.txt",'r',errors='ignore') as f:
            if f.readable():
                self.editBox.delete("1.0","end")
                self.editBox.insert("end",f.read())
    def save_edit(self):
        if self.onEdit:
            markdownText = self.editBox.get("1.0","end")  
            html = markdown2.markdown(markdownText)
            self.savedBox.set_html(html,False)
            self.editBox.pack_forget()
            self.savedBox.pack(fill='both',expand="yes")
            self.button.configure(image=self.editIco)
            self.saveNote()
        else:
            self.savedBox.pack_forget()
            self.editBox.pack(fill='both',expand="yes")
            self.button.configure(image=self.saveIco)
        self.onEdit = not self.onEdit
        
    def change_show_mode(self):
        if self.showMode == "alwaysTop":
            self.showMode = "onDesktop"
            self.button2.configure(image=self.alwaysTopIco)
            self.root.wm_attributes('-topmost',0)  
        elif self.showMode == "onDesktop":
            self.showMode = "alwaysTop"
            self.button2.configure(image=self.onDesktopIco)
            self.root.wm_attributes('-topmost',1)  
       
    def minimize(self):
        self.root.state("iconic")
        
    def loop(self):
        if self.showMode == "alwaysTop":
            self.root.wm_attributes('-topmost',1)
        elif self.showMode == "onDesktop":
            self.root.wm_attributes('-topmost',0)          
           
        if self.root.state() != "iconic":
            self.root.wm_attributes('-toolwindow',1)
        else:
            self.root.wm_attributes('-toolwindow',0)
        self.root.after_cancel(self.afterId)
        self.afterId = self.root.after(50,self.loop) 
   
if __name__ == '__main__':
    myappid = "IRSGame.DesktopNote" # 这里可以设置任意文本
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    NS = NoteSystem() 