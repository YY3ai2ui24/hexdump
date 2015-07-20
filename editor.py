from hexdump import makeDumpList
from tkinter import *
class Application(Frame):
    def createWidgets(self):
        self.menuBar = Menu(self)
        self.configure(menu = self.menuBar)
        self.submenu1 = Menu(self.menuBar, tearoff = False)
        self.submenu2 = Menu(self.menuBar, tearoff = False)
        self.menuBar.add_cascade(label = 'File', underline = 0, menu = submenu1)
        self.menuBar.add_cascade(label = 'Coding', underline = 0, menu = submenu1)
        self.textBox = Message(self)#ダンプテキストを表示するところ
        self.textBox['text'] = 'Select file.'
        self.textBox.pack()
        self.insertButton = Radiobutton(text = 'Insert', variable = self.mode, value = 0)#挿入
        self.insertButton.pack()
        self.deleteButton = Radiobutton(text = 'Delete', variable = self.mode, value = 1)#削除
        self.deleteButton.pack()
        self.sendButton = Button(text='button', command=self.fileEdit)#送信
        self.sendButton.pack()
    def __init__(self, master=None):
        self.mode = 0
        self.currentPos = 0
        self.currentRow = 1j
        self.coding = None
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def fileEdit():
        if self.mode == 0: self.insert()
        elif self.mode == 1: self.delete()
        elif self.mode == 2: self.replace()
    def insert():#insertPos,insertValue
        pass
    def delete():#deletePos
        pass
    def replace():#replacePos,replaceValue
        pass
root = Tk()
app = Application(master=root)
app.mainloop()
