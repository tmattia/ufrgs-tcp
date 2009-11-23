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

from qoc import Element, Criterion, Option, Question

class DiagramElement(Element):
    def __init__(self, description):
        '''Defines a diagram element.
        
        description: diagram element's description
        '''
        Element.__init__(self, description)
        self.color = None
        self.x = None
        self.y = None
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y

class DiagramCriterion(DiagramElement):
    '''Defines a diagram criterion, which is represented as a red square.
    
    description: diagram criterion's description
    '''
    def __init__(self, description):
        DiagramElement.__init__(self, description)
        self.color = (1.0, 0.0, 0.0)

class DiagramOption(DiagramElement):
    '''Defines a diagram option, which is represented as a green square.
    
    description: diagram option's description
    '''
    def __init__(self, description):
        DiagramElement.__init__(self, description)
        self.color = (0.0, 1.0, 0.0)

class DiagramQuestion(DiagramElement):
    '''Defines a diagram question, which is represented as a blue square.
    
    description: diagram question's description
    '''
    def __init__(self, description):
        DiagramElement.__init__(self, description)
        self.color = (0.0, 0.0, 1.0)

class GUI:
    def __init__(self):
        '''Application setup'''
        self.widgetTree = gtk.glade.XML('gui.glade')
        self.widgetTree.signal_autoconnect(self)
        
        self.drawingArea = self.widgetTree.get_widget('drawingarea1')
        self.drawingArea.connect('expose-event', self.draw)
        
        self.statusbar = self.widgetTree.get_widget('statusbar1')
        
        self.mainWindow = self.widgetTree.get_widget('window1')
        self.mainWindow.show_all()
        
        self.elements = []
        
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
        self.currentStatus = self.NOP
    
    def draw(self, widget, event):
        '''Draws the diagram elements in the drawing area'''
        cr = self.drawingArea.window.cairo_create()
        for element in self.elements:
            cr.set_source_rgb(element.color[0], element.color[1], element.color[2])
            cr.rectangle(element.x, element.y, 100, 100)
            cr.fill()
    
    def handleKeyboard(self, widget, event):
        '''Handles a keyboard release event on the main window'''
        ESC = 65307
        if self.currentStatus and event.keyval == ESC:
            self.setStatus(self.NOP)
    
    def drawingAreaClick(self, widget, event):
        '''Handles a click event on the drawing area.'''
        opts = [
            self.INSERT_CRITERION,
            self.INSERT_OPTION,
            self.INSERT_QUESTION
        ]
        if event.button == 1 and self.currentStatus in opts:
            self.obj.setPosition(event.x, event.y)
            self.elements.append(self.obj)
            self.setStatus(self.NOP)
            self.draw(widget, event)
                
    
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
        contextId = self.statusbar.get_context_id('status')
        self.statusbar.push(contextId, self.statusMsg[status])
        self.currentStatus = status
        self.obj = obj
    
    def insertCriterion(self, widget):
        '''Inserts a new criterion on the drawing area.'''
        description = self.getTextInput('New criterion', 'Description: ')
        if description:
            c = DiagramCriterion(description)
            self.setStatus(self.INSERT_CRITERION, c)
    
    def insertOption(self, widget):
        '''Inserts a new option on the drawing area.'''
        description = self.getTextInput('New option', 'Description: ')
        if description:
            o = DiagramOption(description)
            self.setStatus(self.INSERT_OPTION, o)
    
    def insertQuestion(self, widget):
        '''Inserts a new question on the drawing area."'''
        description = self.getTextInput('New question', 'Description: ')
        if description:
            q = DiagramQuestion(description)
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
