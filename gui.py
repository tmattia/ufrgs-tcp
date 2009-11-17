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

class GUI:
    def __init__(self):
        '''Application setup'''
        widgetTree = gtk.glade.XML('gui.glade')
        widgetTree.signal_autoconnect(self)
        
        self.mainWindow = widgetTree.get_widget('window1')
        self.mainWindow.show_all()
    
    def drawingAreaClick(self, widget, event):
        '''Handles a click event on the drawing area.'''
        if event.button == 1:
            # left button
            print event.x, event.y
    
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
    
    def insertCriterion(self, widget):
        '''Inserts a new criterion on the drawing area.'''
        print 'criterion'
    
    def insertOption(self, widget):
        '''Inserts a new option on the drawing area.'''
        print 'option'
    
    def insertQuestion(self, widget):
        '''Inserts a new question on the drawing area."'''
        print 'question'
    
    def insertRelationship(self, widget):
        '''Inserts a new relationship on the drawing area.'''
        print 'relationship'

if __name__ == '__main__':
    '''If the script is run directly through a command line (e.g.
    `python gui.py`), opens the interface window.'''
    GUI()
    gtk.main()
