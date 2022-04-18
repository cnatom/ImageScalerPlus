from fileinput import filename
import os, sys
import os.path
import string
import threading
import tkinter
from tkinter import dialog
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image

class ImageScaler(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.rowList = []
        self.savePath = ""
        self.initializeWindow()
    def initializeWindow(self):
        self.grid()
        #导入图片
        self.openButton = tkinter.Button(self,text=u"导入图片",command=self.onOpenButtonClick)
        self.openButton.grid(column=0,row=1,columnspan=3,sticky="ew")
        #路径显示
        self.openVar   = tkinter.StringVar()
        self.openVar.set("")
        self.openLabel = tkinter.Label(self,textvariable=self.openVar,anchor="c",bg="gray")
        self.openLabel.grid(column=0,row=2,columnspan=3,sticky="ew")
        #缩放文本
        self.scaleLabel = tkinter.Label(self,anchor="c",text="倍率")
        self.scaleLabel.grid(column=0,row=6,columnspan=1,sticky="ew")
        #缩放滑动条
        self.scaleList = [5,10,15,20,25,50,75]
        self.scaleVar  = tkinter.IntVar()
        self.scaleVar.set(50)
        self.scaleMenu = tkinter.OptionMenu(self,self.scaleVar,*self.scaleList)
        self.scaleMenu.config(width=20)
        self.scaleMenu.grid(column=1,row=6,stick="ew")
        #处理
        self.scaleButton = tkinter.Button(self,text=u"处理并导出",command=self.onScaleButtonClick)
        self.scaleButton.grid(column=2,row=6,columnspan=1,sticky="ew")
        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False)
    # 选择保存位置
    def setSavePath(self):
        self.savePath = tkinter.filedialog.askdirectory()
    # 打开图片
    def onOpenButtonClick(self):
        imageTypes = [("Image files",("*.png","*.jpg","*.jpeg","*.gif")), ("All files", "*")]
        fileDialog = tkinter.filedialog.Open(self, filetypes = imageTypes)
        fileName = fileDialog.show()
        if fileName.lower().endswith((".png",".jpg",".jpeg",".gif")):
            self.rowList.append(fileName)
            self.openVar.set(fileName+"\n"+self.openVar.get())
        else:
            self.showError("无效文件类型!")
            self.clearFileInfo()
    # 点击处理
    def onScaleButtonClick(self):
        self.setSavePath()
        
        # 多线程处理并保存
        threads = []
        for row in self.rowList:
            t = threading.Thread(target=self.handleThread(row))
            threads.append(t)
        for t in threads:
            t.start()
    
        self.showInfo("保存成功！")
        self.savePath = ""
        self.rowList.clear()
        self.openVar.set(" ")
    def handleThread(self,row):
        name = row.split("/")[-1]
        self.scaleFile(row).save(self.savePath+"/"+name)
    def scaleFile(self,imageName):
        image = Image.open(imageName)
        size  = image.size
        sizeX = size[0]
        sizeY = size[1]
        scaleFactor = self.scaleVar.get()
        newSizeX    = sizeX*(scaleFactor*0.01)
        newSizeY    = sizeY*(scaleFactor*0.01)
        newSize     = (newSizeX,newSizeY)
        if newSizeX < 1 or newSizeY < 1:
            self.showError("图片太小了，无法继续缩放！")
            return None
        image.thumbnail(newSize)
        return image

    def showError(self, message):
        tkinter.messagebox.showerror("Error",message)

    def showInfo(self, message):
        tkinter.messagebox.showinfo("Info",message)

if __name__ == "__main__":
    app = ImageScaler(None)
    app.title("多线程图像缩放")
    app.mainloop()