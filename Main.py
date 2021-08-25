from posixpath import commonpath
from tkinter import *
import os, time

class Notepad(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry('700x400+250+250')
        self.title('Untitled - Notepad')

    def menuBar(self):
        self.mainMenu = Menu(self, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.config(menu=self.mainMenu)
    
    def addFileMenu(self):
        self.fileMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.fileMenu.add_command(label='New', command=lambda : os.startfile('Main.py'), accelerator='Ctrl+N')
        self.fileMenu.add_command(label='Open...', accelerator='Ctrl+O')
        self.fileMenu.add_command(label='Save', accelerator='Ctrl+S')
        self.fileMenu.add_command(label='Save As...')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=quit)
        self.mainMenu.add_cascade(label='File', menu=self.fileMenu)

    def addEditMenu(self):
        self.editMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0,)
        self.editMenu.add_command(label='Undo', command=lambda: self.textBox.event_generate('<<Undo>>'), accelerator='Ctrl+Z')
        self.editMenu.add_command(label='Redo', command=lambda: self.textBox.event_generate('<<Redo>>'), accelerator='Ctrl+Y')
        self.editMenu.add_separator()
        self.editMenu.add_command(label='Cut', command=lambda: self.textBox.event_generate('<<Cut>>'), accelerator='Ctrl+X')
        self.editMenu.add_command(label='Copy', command=lambda: self.textBox.event_generate('<<Copy>>'), accelerator='Ctrl+C')
        self.editMenu.add_command(label='Paste', command=lambda: self.textBox.event_generate('<<Paste>>'), accelerator='Ctrl+V')
        self.editMenu.add_command(label='Delete', command=self.__delete, accelerator=' '*6+'Del')
        self.editMenu.add_separator()
        self.editMenu.add_command(label='Select All', command=lambda: self.textBox.tag_add(SEL, '1.0', END), accelerator='Ctrl+A')
        self.editMenu.add_command(label='Time/Date', command=lambda: self.textBox.insert('insert', time.asctime(time.localtime())), accelerator=' '*8+'F5')
        self.mainMenu.add_cascade(label='Edit', menu=self.editMenu)

    def addFormatMenu(self):
        self.formatMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.wordWrap = IntVar()
        self.wordWrap.set(1)
        self.formatMenu.add_checkbutton(label='Word Wrap', variable=self.wordWrap, command=self.wordWrap_)
        self.formatMenu.add_command(label='Font...')
        self.mainMenu.add_cascade(label='Format', menu=self.formatMenu)

    def addViewMenu(self):
        self.viewMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.statusBarCheck = IntVar()
        self.statusBarCheck.set(0)
        self.viewMenu.add_checkbutton(label='Status Bar', variable=self.statusBarCheck, command=self.statusBar_)
        self.mainMenu.add_cascade(label='View', menu=self.viewMenu)

    def addHelpMenu(self):
        self.helpMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.helpMenu.add_command(label='View Help')
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label='About Notepad')
        self.mainMenu.add_cascade(label='Help', menu=self.helpMenu)

    def addTextBox(self):
        self.textBox = Text(self, bd=0, wrap=WORD, font=('Consolas', 20), highlightthickness=0, relief=FLAT, selectborderwidth=0, padx=8, pady=3, selectforeground='white', undo=True)
        self.textBox.pack(fill=BOTH, expand=YES, side=RIGHT, pady=1)
        self.textBoxinfo = self.textBox.pack_info()
        self.verticalScrollbar.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=self.verticalScrollbar.set, xscrollcommand=self.horizontalScrollbar.set)
        self.horizontalScrollbar.config(command=self.textBox.xview)
        if self.wordWrap.get():
            self.textBox.config(wrap=WORD)
        else:
            self.textBox.config(wrap=NONE)
        self.textBox.focus()

    def addVerticalScrollbar(self):
        self.verticalScrollbar = Scrollbar(self, orient=VERTICAL, bd=0, relief=FLAT)
        self.verticalScrollbar.pack(fill=Y, expand=NO, side=RIGHT, pady=1)
        self.verticalScrollbarinfo = self.verticalScrollbar.pack_info()

    def addHorizontalScrollbar(self):
        self.horizontalScrollbar = Scrollbar(self, orient=HORIZONTAL, bd=0, relief=FLAT)
        self.horizontalScrollbar.pack(side=BOTTOM, expand=YES, fill=X, anchor=CENTER)
        self.horizontalScrollbarinfo = self.horizontalScrollbar.pack_info()
        self.horizontalScrollbar.pack_forget()

    def updateNotepad(self):
        if self.statusBarCheck.get() and not self.wordWrap.get():
            self.statusBar.pack(self.statusBarinfo)
        if not self.wordWrap.get():
            self.horizontalScrollbar.pack(self.horizontalScrollbarinfo)
        self.verticalScrollbar.pack(self.verticalScrollbarinfo)
        self.textBox.pack(self.textBoxinfo)

    def addStatusBar(self):
        self.statusBar = Label(self, text='Status', anchor=E)
        self.statusBar.pack(side=BOTTOM, expand=YES, fill=X, anchor=CENTER)
        self.statusBarinfo = self.statusBar.pack_info()
        self.statusBar.pack_forget()

    def __delete(self):
        try:
            if not self.textBox.selection_get():
                pass
            else:
                self.textBox.event_generate('<BackSpace>')
        except:
            pass

    def wordWrap_(self):
        if self.wordWrap.get():
            self.textBox.config(wrap=WORD)
            self.horizontalScrollbar.pack_forget()
            self.statusBar.pack_forget()
        else:
            self.textBox.config(wrap=NONE)
            self.updateNotepad()
    
    def statusBar_(self):
        if self.statusBarCheck.get() and not self.wordWrap.get():
            self.updateNotepad()
        else:
            self.statusBar.pack_forget()

if __name__ == '__main__':
    notepad = Notepad()
    notepad.menuBar()
    notepad.addFileMenu()
    notepad.addEditMenu()
    notepad.addFormatMenu()
    notepad.addViewMenu()
    notepad.addHelpMenu()
    notepad.addStatusBar()
    notepad.addHorizontalScrollbar()
    notepad.addVerticalScrollbar()
    notepad.addTextBox()
    notepad.mainloop()