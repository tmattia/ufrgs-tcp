#!/usr/bin/env python
#-*- coding:utf-8 -*-

try:
    import pygtk
    pygtk.require('2.0')
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

from qoc import Criterion, Option, Question

class GUI:
    def __init__(self):
        '''Application setup'''
        self.widgetTree = gtk.glade.XML('gui.glade')
        self.widgetTree.signal_autoconnect(self)
        
        self.drawingArea = self.widgetTree.get_widget('drawingarea1')
        
        self.statusbar = self.widgetTree.get_widget('statusbar1')
        
        self.mainWindow = self.widgetTree.get_widget('window1')
        self.mainWindow.show_all()
        
        self.NOP = 0
        self.INSERT_CRITERION = 1
        self.INSERT_OPTION = 2
        self.INSERT_QUESTION = 3
        self.statusMsg = {
            self.NOP: '',
            self.INSERT_CRITERION: 'Inserting new Criterion. Press "Esc" to cancel.',
            self.INSERT_OPTION: 'Inserting new Option. Press "Esc" to cancel.',
            self.INSERT_QUESTION: 'Inserting new Question. Press "Esc" to cancel.',
        }
        self.statusHandlers = {
            self.INSERT_CRITERION: self.drawRectangle,
            self.INSERT_OPTION: self.drawRectangle,
            self.INSERT_QUESTION: self.drawRectangle,
        }
        self.currentStatus = self.NOP
    
    def drawRectangle(self, event):
        '''Draws a rectangle on the drawing area from a given mouse click event
        
        event: the mouse click event'''
        print event.x, event.y
        
        cr = self.drawingArea.window.cairo_create()
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(event.x, event.y, 100, 100)
        cr.fill()
    
    def handleKeyboard(self, widget, event):
        '''Handles a keyboard release event on the main window'''
        if event.keyval == 65307:
            if self.currentStatus:
                self.setStatus(self.NOP)
    
    def drawingAreaClick(self, widget, event):
        '''Handles a click event on the drawing area.'''
        if event.button == 1:
            # left button
            print event.x, event.y
            
            if self.currentStatus in self.statusHandlers:
                self.statusHandlers[self.currentStatus](event)
                
    
    def new(self, widget):
        '''Creates a new diagram.'''
        print 'new'
    
    def openFile(self, widget):
        '''Opens an existing diagram.'''
        print 'open'
    
    def save(self, widget):
        '''Saves the current working diagram.'''
        print 'save'
    
    def saveAs(self, widget):
        '''Saves the current working diagram as a different file.'''
        print 'save as'

    def quit(self, widget):
        '''Quits the application.'''
        gtk.main_quit()
    
    def about(self, widget):
        '''Shows "about" information.'''
        print 'about'
    
    def setStatus(self, status, obj=None):
        '''Defines the application status and writes a message on the statusbar.
        Also, optionally holds an object until the next setStatus call.
        
        status: the status code'''
        contextId = self.statusbar.get_context_id('teste')
        self.statusbar.push(contextId, self.statusMsg[status])
        self.currentStatus = status
        self.obj = obj
    
    def insertCriterion(self, widget):
        '''Inserts a new criterion on the drawing area.'''
        description = self.getTextInput('New criterion', 'Description: ')
        if description:
            c = Criterion(description)
            self.setStatus(self.INSERT_CRITERION, c)
    
    def insertOption(self, widget):
        '''Inserts a new option on the drawing area.'''
        description = self.getTextInput('New option', 'Description: ')
        if description:
            o = Option(description)
            self.setStatus(self.INSERT_OPTION, o)
    
    def insertQuestion(self, widget):
        '''Inserts a new question on the drawing area."'''
        description = self.getTextInput('New question', 'Description: ')
        if description:
            q = Question(description)
            self.setStatus(self.INSERT_QUESTION, q)
    
    def insertRelationship(self, widget):
        '''Inserts a new relationship on the drawing area.'''
        print 'relationship'
    
    def getTextInput(self, title, labelText):
        '''Shows a dialog window with a text entry. Returns a string with the
        text entry value.
        
        title: window title
        labelText: text applied to the entry's label
        '''
        label = self.widgetTree.get_widget('textInputLabel')
        label.set_text(labelText)
        
        dialog = self.widgetTree.get_widget('textInputDialog')
        dialog.set_title(title)
        
        entry = self.widgetTree.get_widget('textInputEntry')
        entry.grab_focus()
        
        response = dialog.run()
        dialog.hide()
        
        text = ''
        if response == 1:
            text = entry.get_text()
        entry.set_text('')
        return text
    
    def textInputDialogOk(self, widget):
        '''Handles the dialog's ok button event.'''
        dialog = self.widgetTree.get_widget('textInputDialog')
        dialog.response(1)
    
    def textInputDialogCancel(self, widget):
        '''Handles the dialog's cancel button event.'''
        dialog = self.widgetTree.get_widget('textInputDialog')
        dialog.response(0)

if __name__ == '__main__':
    '''If the script is run directly through a command line (e.g.
    `python gui.py`), opens the interface window.'''
    GUI()
    gtk.main()
