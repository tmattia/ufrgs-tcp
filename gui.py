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
    import sys
    sys.exit(1)

from qoc import *
from diagram import *
from keyboard_codes import *
import pickle

class GUI:
    def __init__(self):
        '''Defines the diagram's GUI.'''
        self.widgetTree = gtk.glade.XML('gui.glade')
        self.widgetTree.signal_autoconnect(self)
        
        drawingArea = self.widgetTree.get_widget('drawingarea1')
        self.diagram = Diagram(drawingArea)
        
        self.statusbar = self.widgetTree.get_widget('statusbar1')
        
        mainWindow = self.widgetTree.get_widget('window1')
        mainWindow.show_all()
        
        self.currentStatus = None
        self.obj = None
        
        self.NOP = 0
        self.INSERT_CRITERION = 1
        self.INSERT_OPTION = 2
        self.INSERT_QUESTION = 3
        self.INSERT_RELATIONSHIP = 4
        self.SELECTED_ELEMENT = 5
        self.statusMsg = {
            self.NOP: '',
            self.INSERT_CRITERION: 'Inserting new Criterion. Press "Esc" to cancel.',
            self.INSERT_OPTION: 'Inserting new Option. Press "Esc" to cancel.',
            self.INSERT_QUESTION: 'Inserting new Question. Press "Esc" to cancel.',
            self.INSERT_RELATIONSHIP: 'Select two elements to insert a new Relationship. Press "Esc" to cancel.',
            self.SELECTED_ELEMENT: 'Selected element. Press "Esc" to cancel.'
        }
        self.setStatus(self.NOP)
    
    def setStatus(self, status, obj=None):
        '''Defines the application status and writes a message on the statusbar.
        Also, optionally holds an object until the next setStatus call.
        
        status: the status code'''
        contextId = self.statusbar.get_context_id('status')
        self.statusbar.push(contextId, self.statusMsg[status])
        self.currentStatus = status
        self.obj = obj
    
    def handleKeyboard(self, widget, event):
        '''Handles a keyboard release event on the main window'''
        if self.currentStatus != self.NOP and event.keyval == ESC:
            self.setStatus(self.NOP)
        elif self.currentStatus == self.SELECTED_ELEMENT:
            if event.keyval == DELETE:
                self.diagram.removeElement(self.obj)
                self.setStatus(self.NOP)
            elif event.keyval in [LEFT, UP, RIGHT, DOWN]:
                self.diagram.moveElement(self.obj, event.keyval)
    
    def handleClick(self, widget, event):
        '''Handles a click event on the drawing area.'''
        opts = [
            self.INSERT_CRITERION,
            self.INSERT_OPTION,
            self.INSERT_QUESTION
        ]
        if self.currentStatus in opts:
            self.diagram.addElement(self.obj, event.x, event.y)
            self.setStatus(self.NOP)
            
        elif self.currentStatus == self.NOP:
            el = self.diagram.selectElement(event.x, event.y)
            if el:
                self.setStatus(self.SELECTED_ELEMENT, el)
            
        elif self.currentStatus == self.INSERT_RELATIONSHIP:
            if self.obj is None:
                self.obj = self.diagram.selectElement(event.x, event.y)
                if not isinstance(self.obj, Relational):
                    print 'primeiro objeto tem que ser relacional'
                    self.setStatus(self.NOP)
            else:
                el = self.diagram.selectElement(event.x, event.y)
                if el:
                    try:
                        self.diagram.addRelationship(self.obj, el,
                            event.button == 1)
                    except RelationshipAlreadyExists:
                        print 'ja existe'
                    except RelationshipNotPossible:
                        print 'nao pode relacao'
                    self.setStatus(self.NOP)
    
    def new(self, widget=None):
        '''Creates a new diagram.'''
        while len(self.diagram.elements):
            el = self.diagram.elements[0]
            self.diagram.removeElement(el)
        self.diagram.draw()
    
    def openFile(self, widget):
        '''Opens an existing diagram.'''
        filename = self.getTextInput('Open file', 'Full path: ')
        if filename:
            try:
                f = open(filename, 'r')
                loadObj = pickle.load(f)
                self.diagram.elements, self.diagram.relationships = loadObj
                f.close()
                self.diagram.draw()
            except Exception, e:
                print 'Erro ao abrir', e
    
    def save(self, widget):
        '''Saves the current working diagram.'''
        filename = self.getTextInput('Save file', 'Full path: ')
        if filename:
            try:
                saveObj = (self.diagram.elements, self.diagram.relationships)
                f = open(filename, 'w')
                pickle.dump(saveObj, f)
                f.close()
            except Exception, e:
                print 'Erro ao salvar', e

    def quit(self, widget):
        '''Quits the application.'''
        gtk.main_quit()
    
    def about(self, widget):
        '''Shows "about" information.'''
        print 'about'
    
    def handleInsertCriterion(self, widget):
        '''Inserts a new criterion on the drawing area.'''
        description = self.getTextInput('New criterion', 'Description: ')
        if description:
            c = DiagramCriterion(description)
            self.setStatus(self.INSERT_CRITERION, c)
    
    def handleInsertOption(self, widget):
        '''Inserts a new option on the drawing area.'''
        description = self.getTextInput('New option', 'Description: ')
        if description:
            o = DiagramOption(description)
            self.setStatus(self.INSERT_OPTION, o)
    
    def handleInsertQuestion(self, widget):
        '''Inserts a new question on the drawing area."'''
        description = self.getTextInput('New question', 'Description: ')
        if description:
            q = DiagramQuestion(description)
            self.setStatus(self.INSERT_QUESTION, q)
    
    def handleInsertRelationship(self, widget):
        '''Inserts a new relationship on the drawing area.'''
        self.setStatus(self.INSERT_RELATIONSHIP)
    
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
