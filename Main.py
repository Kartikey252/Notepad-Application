# Importing tkinter, tkfontchooser, os and Datetime Modules
from tkinter import *
from tkinter.font import Font
import tkinter.messagebox as tmsg
import tkinter.filedialog as tkfile
from tkfontchooser import askfont
import os, datetime

# Creating a Notepad Class
class Notepad(Tk):

    # Name of File Opened
    __filename = ''

    def __init__(self) -> None:
        """ Takes Methods From Tk Class of Tkinter Module """
        super().__init__()
        self.geometry('700x400+250+250')
        self.title('Untitled - Notepad')

    def menuBar(self) -> None:
        """ Adds Menubar in App """
        self.mainMenu = Menu(self, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.config(menu=self.mainMenu)
    
    def addFileMenu(self) -> None:
        """ Adds File Menu in Menubar 
        File Menu Contains:
            New -> Make App Run From Beginning
            Open -> Opens A File
            Save -> Saves File
            Save As.. -> Saves File as a New One, even if File Exists
            Exit -> Quits Application
        """
        self.fileMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.fileMenu.add_command(label='New', command=self.__startNotepad, accelerator='Ctrl+N')
        self.fileMenu.add_command(label='Open...', accelerator='Ctrl+O', command=self.__openFileNotepad)
        self.fileMenu.add_command(label='Save', accelerator='Ctrl+S', command=self.__saveFile)
        self.fileMenu.add_command(label='Save As...', command=lambda : self.__saveFile(saveAs=True))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=self.__whenExit)
        self.mainMenu.add_cascade(label='File', menu=self.fileMenu)

    def addEditMenu(self) -> None:
        """ Adds Edit Menu in Menubar 
        Edit Menu Contains:
            Undo -> Erases last change in document
            Redo -> Redoes the Erased change in document
            Cut -> Cuts the Selected Part
            Copy -> Copies the Selected Part
            Paste -> Paste the Copy/Cut part
            Delete -> Deletes the Selected Part
            Select All -> Selects all Document
            Time/Date -> Enters Time And Date in Document
                Format-> {Hour:Minutes Date-Month-Year}
        """
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
        """ Adds Format Menu in Menubar 
        Format Menu Contains:
            Word Wrap -> Enables/Disables Word Wrap Function
            Font... -> Change Font of Document
        """
        self.formatMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.wordWrap = IntVar()
        self.wordWrap.set(1)
        self.formatMenu.add_checkbutton(label='Word Wrap', variable=self.wordWrap, command=self.__wordWrap_)
        self.formatMenu.add_command(label='Font...', command=self.__Font)
        self.mainMenu.add_cascade(label='Format', menu=self.formatMenu)

    def addViewMenu(self):
        """ Adds View Menu in Menubar 
        View Menu Contains:
            Status Bar -> Shows/Hides Status Bar
        """
        self.viewMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.statusBarCheck = IntVar()
        self.statusBarCheck.set(0)
        self.viewMenu.add_checkbutton(label='Status Bar', variable=self.statusBarCheck, command=self.__statusBar_)
        self.mainMenu.add_cascade(label='View', menu=self.viewMenu)

    def addHelpMenu(self):
        """ Adds Help Menu in Menubar 
        Help Menu Contains:
            View Help -> Shows Help For Application
            About Notepad -> Tells About Notepad
        """
        self.helpMenu = Menu(self.mainMenu, tearoff=0, relief=FLAT, activebackground='#82caff', activeforeground='black', bd=0)
        self.helpMenu.add_command(label='View Help', command=self.__helpNotepad)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label='About Notepad', command=self.__aboutNotepad)
        self.mainMenu.add_cascade(label='Help', menu=self.helpMenu)

    def addTextBox(self):
        """ Adds TextBox in App """
        self.textBox = Text(self, bd=0, wrap=WORD, font=('Consolas', 20), highlightthickness=0, relief=FLAT, selectborderwidth=0, padx=8, pady=3, selectforeground='white', undo=True, border=0, borderwidth=0)
        self.textBox.pack(fill=BOTH, expand=YES, side=RIGHT, pady=0.1)
        self.textFont = {'family':'Consolas', 'size':20, 'weight':'normal', 'slant':'roman', 'underline':0, 'overstrike':0}
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
        """ Adds Vertical Scrollbar For Textbox """
        self.verticalScrollbar = Scrollbar(self, orient=VERTICAL, bd=0, relief=FLAT)
        self.verticalScrollbar.pack(fill=Y, expand=NO, side=RIGHT, pady=1)
        self.verticalScrollbarinfo = self.verticalScrollbar.pack_info()

    def addHorizontalScrollbar(self):
        """ Adds Horizontal Scrollbar For Textbox """
        self.horizontalScrollbar = Scrollbar(self, orient=HORIZONTAL, bd=0, relief=FLAT)
        self.horizontalScrollbar.pack(side=BOTTOM, expand=YES, fill=X, anchor=CENTER)
        self.horizontalScrollbarinfo = self.horizontalScrollbar.pack_info()
        self.horizontalScrollbar.pack_forget()

    def __updateNotepad(self):
        """ Udates Notepad Every time When Selects 'Word Wrap' Or 'Status Bar' Option"""
        if self.statusBarCheck.get() and not self.wordWrap.get():
            self.statusBar.pack(self.statusBarinfo)
        if not self.wordWrap.get():
            self.horizontalScrollbar.pack(self.horizontalScrollbarinfo)
        self.verticalScrollbar.pack(self.verticalScrollbarinfo)
        self.textBox.pack(self.textBoxinfo)

    def addStatusBar(self):
        """ Add Status Bar to App """
        self.statusBar = Label(self, text='Status', anchor=E)
        self.statusBar.pack(side=BOTTOM, expand=YES, fill=X, anchor=CENTER)
        self.statusBarinfo = self.statusBar.pack_info()
        self.statusBar.pack_forget()

    def __delete(self):
        """ Deletes the Selected Part """
        try:
            if not self.textBox.selection_get():
                pass
            else:
                self.textBox.event_generate('<BackSpace>')
        except:
            pass

    def __Datetime(self, event=None):
        """ Enters Time And Date in Document
                Format-> {Hour:Minutes Date-Month-Year} """
        self.__delete()
        self.textBox.insert('insert', datetime.datetime.now().strftime('%H:%M %d-%m-%Y'))

    def __wordWrap_(self):
        """ Enables/Disables Word Wrap Function """
        if self.wordWrap.get():
            self.textBox.config(wrap=WORD)
            self.horizontalScrollbar.pack_forget()
            self.statusBar.pack_forget()
        else:
            self.textBox.config(wrap=NONE)
            self.__updateNotepad()
    
    def __statusBar_(self):
        """ Shows/Hides Status Bar in App """
        if self.statusBarCheck.get() and not self.wordWrap.get():
            self.__updateNotepad()
        else:
            self.statusBar.pack_forget()
    
    def statusBarUpdate(self):
        """ Updates Status Bar after Each 2 Mili Seconds"""
        pos = self.textBox.index(INSERT).split('.')
        pos = f'Ln {pos[0]}, Col {int(pos[1])+1}'+' '*30
        self.statusBar.config(text=pos)
        self.after(2, self.statusBarUpdate)

    def __helpNotepad(self):
        """ Shows Help For Application """
        tmsg.showinfo('Help', 'This Key Only in Construction, Wait For Website')

    def __aboutNotepad(self):
        """ Tells About Notepad """
        tmsg.showinfo('About Notepad', 'This is a Notepad made by a Loser In Free Time.')

    def __newNote(self):
        """ New Document """
        self.textBox.delete("0.0", END)
        self.title('Untitled - Notepad')
        self.__filename = ''

    def __startNotepad(self, event=None):
        """ Make App Run From Beginning """
        if self.__filename:
            with open(self.__filename, 'r') as f:
                txt = f.read()
            if txt+'\n' == self.textBox.get("1.0", END):
                self.__newNote()
            else:
                self.__actionForFile(self.__newNote)
        else:
            if self.textBox.get("1.0", END) == '\n':
                self.__newNote()
            else:
                self.__actionForFile(self.__newNote)

    def __openNote(self):
        """ Opens File """
        try:
            filename = tkfile.askopenfilename()
            with open(filename, 'r') as f:
                txt = f.read()
            self.textBox.delete("1.0", END)
            self.textBox.insert("1.0", txt)
            self.title(f'{filename} - Notepad')
            self.__filename = filename
        except:
            pass

    def __openFileNotepad(self, event=None):
        """ Opens A File """
        if self.__filename:
            with open(self.__filename, 'r') as f:
                txt = f.read()
            if txt+'\n' == self.textBox.get("1.0", END):
                self.__openNote()
            else:
                self.__actionForFile(self.__openNote)
        else:
            if self.textBox.get("1.0", END) == '\n':
                self.__openNote()
            else:
                self.__actionForFile(self.__openNote)

    def __saveFile(self, event=None, saveAs=False):
        """ Save File
        parametes :
            SaveAs == True
                Run Function for Save As Function
            SaveAs == False
                Run Function for Save Only
        """
        if self.__filename and not saveAs:
            with open(self.__filename, 'w') as f:
                f.write(self.textBox.get("1.0", END)[:-1])
            return True
        try:
            filename = tkfile.asksaveasfilename()
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.textBox.get("1.0", END)[:-1])
                self.title(f'{filename} - Notepad')
                self.__filename = filename
                return True
            else:
                return False
        except:
            return False

    def __actionForFile(self, funcToPerform):
        """ Perform Action Pass As its Parameter.
        Asks for Saving File And Then Perform the Passed Function.
        """
        dialog = tmsg.askyesnocancel('Notepad', 'Do you want to save this file ?')
        if dialog == None:
            pass
        elif dialog == False:
            funcToPerform()
        else:
            saved = self.__saveFile()
            if saved:
                funcToPerform()

    def __whenExit(self, event=None):
        """ Performed When Exitting App """
        if self.__filename:
            with open(self.__filename, 'r') as f:
                txt = f.read()
            if txt == self.textBox.get("1.0", END)[:-1]:
                self.quit()
            else:
                self.__actionForFile(self.quit)
        else:
            if self.textBox.get("1.0", END) == '\n':
                self.quit()
            else:
                self.__actionForFile(self.quit)

    def bindKeys(self):
        """ Adding Key Shortcuts To App """
        self.bind('<Control-n>', self.__startNotepad)
        self.bind('<Control-o>', self.__openFileNotepad)
        self.bind('<Control-s>', self.__saveFile)
        self.bind('<Control-Shift-s>', lambda x : self.__saveFile(saveAs=True))
        self.protocol('WM_DELETE_WINDOW', self.__whenExit)
        self.bind('<F5>', self.__Datetime)
        self.bind('<Control-z>', lambda x: self.textBox.event_generate('<<Undo>>'))
        self.bind('<Control-y>', lambda x: self.textBox.event_generate('<<Redo>>'))
        self.bind('<Control-x>', lambda x: self.textBox.event_generate('<<Cut>>'))
        self.bind('<Control-c>', lambda x: self.textBox.event_generate('<<Copy>>'))
        self.bind('<Control-v>', lambda x: self.textBox.event_generate('<<Paste>>'))
        self.bind('<Control-a>', lambda x: self.textBox.tag_add(SEL, '1.0', END))

    def __Font(self):
        font = askfont(self, "ABCD abcd", title='Font', family=self.textFont['family'], size=self.textFont['size'], weight=self.textFont['weight'], slant=self.textFont['slant'], underline=self.textFont['underline'], overstrike=self.textFont['overstrike'])
        if font:
            font_ = Font(family=font['family'], size=font['size'], weight=font['weight'], slant=font['slant'], underline=font['underline'], overstrike=font['overstrike'])
            self.textBox.config(font=font_)
            self.textFont = font

        

if __name__ == '__main__':
    print("Please Run 'Notepad.py'\n")
    input()