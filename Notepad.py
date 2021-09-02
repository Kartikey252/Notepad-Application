# Import Notepad Class from Main.py
from Main import Notepad


# Creating App using Notepad Class

App = Notepad() 
App.menuBar() # Creating Main Menu
App.addFileMenu() # Adding File Menu
App.addEditMenu() # Adding Edit Menu
App.addFormatMenu() # Adding Format Menu
App.addViewMenu() # Adding View Menu
App.addHelpMenu() # Adding Help Menu
App.addStatusBar() # Adding Status Bar
App.addHorizontalScrollbar() # Adding The Horizontal Scrollbar
App.addVerticalScrollbar() # Adding The Vertical Scrollbar
App.addTextBox() # Adding Text Box
App.statusBarUpdate() # Updating Status Bar
App.bindKeys() # Adding Key Shortcuts for Certain Functions
App.mainloop() # Add Mainloop for App