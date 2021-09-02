from tkinter import *
import tkinter.messagebox as tmsg
import tkinter.filedialog as tkfile
import os, datetime

class Notepad(Tk):
    
    saveDialogCheck = False
    filename = ''

    def __init__(self) -> None:
        super().__init__()
        self.geometry('700x400+250+250')
        self.title('Untitled - Notepad')

    def menuBar(self):
        self.mainMenu = Menu(self, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.config(menu=self.mainMenu)
    
    def addFileMenu(self):
        self.fileMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.fileMenu.add_command(label='New', command=self.startNotepad, accelerator='Ctrl+N')
        self.fileMenu.add_command(label='Open...', accelerator='Ctrl+O', command=self.openFileNotepad)
        self.fileMenu.add_command(label='Save', accelerator='Ctrl+S', command=self.saveFile)
        self.fileMenu.add_command(label='Save As...', command=lambda : self.saveFile(saveAs=True))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=self.whenExit)
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
        self.editMenu.add_command(label='Time/Date', command=self.__Datetime, accelerator=' '*8+'F5')
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
        self.helpMenu.add_command(label='View Help', command=self.helpNotepad)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label='About Notepad', command=self.aboutNotepad)
        self.mainMenu.add_cascade(label='Help', menu=self.helpMenu)

    def addTextBox(self):
        self.textBox = Text(self, bd=0, wrap=WORD, font=('Consolas', 20), highlightthickness=0, relief=FLAT, selectborderwidth=0, padx=8, pady=3, selectforeground='white', undo=True)
        self.textBox.pack(fill=BOTH, expand=YES, side=RIGHT, pady=00.1)
        self.textboxFont = {'family':'Consolas', 'size':20, 'weight':'normal', 'slant':'roman', 'underline':0, 'overstrike':0}
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

    def __Datetime(self):
        self.__delete()
        self.textBox.insert('insert', datetime.datetime.now().strftime('%H:%M %d-%m-%Y'))

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
    
    def statusBarUpdate(self):
        pos = self.textBox.index(INSERT).split('.')
        pos = f'Ln {pos[0]}, Col {int(pos[1])+1}'+' '*30
        self.statusBar.config(text=pos)
        self.after(2, self.statusBarUpdate)

    def helpNotepad(self):
        tmsg.showinfo('Help', 'This Key Only in Construction, Wait For Website')

    def aboutNotepad(self):
        tmsg.showinfo('About Notepad', 'This is a Notepad made by a Loser In Free Time.')

    def newNote(self):
        self.textBox.delete("1.0", END)
        self.title('Untitled - Notepad')
        self.filename = ''

    def startNotepad(self):
        if self.filename:
            with open(self.filename, 'r') as f:
                txt = f.read()
            if txt+'\n' == self.textBox.get("1.0", END):
                self.newNote()
            else:
                self.actionForFile(self.newNote)
        else:
            if self.textBox.get("1.0", END) == '\n':
                self.newNote()
            else:
                self.actionForFile(self.newNote)

    def openNote(self):
        try:
            filename = tkfile.askopenfilename()
            with open(filename, 'r') as f:
                txt = f.read()
            self.textBox.delete("1.0", END)
            self.textBox.insert("1.0", txt)
            self.title(f'{filename} - Notepad')
            self.filename = filename
        except:
            pass

    def openFileNotepad(self):
        if self.filename:
            with open(self.filename, 'r') as f:
                txt = f.read()
            if txt+'\n' == self.textBox.get("1.0", END):
                self.openNote()
            else:
                self.actionForFile(self.openNote)
        else:
            if self.textBox.get("1.0", END) == '\n':
                self.openNote()
            else:
                self.actionForFile(self.openNote)

    def saveFile(self, saveAs=False):
        if self.filename and not saveAs:
            with open(self.filename, 'w') as f:
                f.write(self.textBox.get("1.0", END)[:-1])
            return True
        try:
            filename = tkfile.asksaveasfilename()
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.textBox.get("1.0", END)[:-1])
                self.title(f'{filename} - Notepad')
                self.filename = filename
                return True
            else:
                return False
        except:
            return False

    def actionForFile(self, funcToPerform):
        dialog = tmsg.askyesnocancel('Notepad', 'Do you want to save this file ?')
        if dialog == None:
            pass
        elif dialog == False:
            funcToPerform()
        else:
            saved = self.saveFile()
            if saved:
                funcToPerform()

    def whenExit(self):
        if self.filename:
            with open(self.filename, 'r') as f:
                txt = f.read()
            if txt == self.textBox.get("1.0", END)[:-1]:
                self.quit()
            self.actionForFile(self.quit)
        else:
            if self.textBox.get("1.0", END) == '\n':
                self.quit()
            self.quit()

        

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
    notepad.statusBarUpdate()
    notepad.mainloop()