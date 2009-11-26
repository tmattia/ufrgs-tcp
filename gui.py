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

import cairo
from qoc import Element, Criterion, Option, Question, Relational, \
    Relationship,RelationshipNotPossible, RelationshipAlreadyExists
from math import pi

# keyboard event codes
ESC = 65307
DELETE = 65535
LEFT = 65361
UP = 65362
RIGHT = 65363
DOWN = 65364

class ElementIsNotRelational(Exception):
    '''Exception signalizing that a given element is not relational.'''
    pass

class DiagramRelationship(Relationship):
    def __init__(self, elementA, elementB, pro=True):
        '''Defines a directional diagram relationship from the first to the
        second element.
        
        elementA: first element
        elementB: second element'''
        elementA.addRelationship(elementB, pro)
        Relationship.__init__(self, elementA, elementB)
        if self.pro:
            self.color = (0.5, 0.5, 0.5)
        else:
            self.color = (1.0, 1.0, 1.0)
    
    def hasPoint(self, x, y):
        return False
    
    def draw(self, cr):
        '''Draws the relationship.
        
        cr: cairo context in which the relationship will be drawn
        '''
        cr.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cr.move_to(self.elementA.x + self.elementA.width / 2,
            self.elementA.y + self.elementA.height / 2)
        cr.line_to(self.elementB.x + self.elementB.width / 2,
            self.elementB.y + self.elementB.height / 2)
        cr.stroke()
        

class DiagramElement(object):
    def __init__(self):
        '''Defines a diagram element.'''
        self.color = None
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        
        self.FONT_FACE = 'Monospace'
        self.FONT_SIZE = 13
        self.FONT_COLOR = (0.0, 0.0, 0.0)
        self.LINE_LENGTH = 30
        self.LINE_HEIGHT = 10
        self.LINE_PADDING = 5
        self.CHAR_WIDTH = 8
    
    def setPosition(self, x, y):
        '''Defines the element position.
        
        x: x coordinate
        y: y coordinate
        '''
        self.x = x
        self.y = y
    
    def hasPoint(self, x, y):
        return (x > self.x and x < (self.x + self.width) \
            and y > self.y and y < (self.y + self.height))
    
    def draw(self, cr):
        '''Draws the element.
        
        cr: cairo context in which the element will be drawn
        '''
        cr.select_font_face(self.FONT_FACE, cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(self.FONT_SIZE)
        
        textlen = len(self.description)
        
        if not self.width:
            self.width = self.CHAR_WIDTH * 2
            if textlen > self.LINE_LENGTH:
                self.width += self.LINE_LENGTH * self.CHAR_WIDTH
            else:
                self.width += textlen * self.CHAR_WIDTH
        
        if not self.height:
            self.height = ((textlen / self.LINE_LENGTH) + 1) * \
                (self.LINE_HEIGHT + self.LINE_PADDING) + (self.LINE_PADDING * 2)
        
        cr.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cr.rectangle(self.x, self.y, self.width, self.height)
        cr.fill()
        
        cr.set_source_rgb(self.FONT_COLOR[0], self.FONT_COLOR[1],
            self.FONT_COLOR[2])
        if textlen > self.LINE_LENGTH:
            for i in xrange(textlen / self.LINE_HEIGHT):
                cr.move_to(self.x + self.CHAR_WIDTH,
                    self.y + (self.LINE_HEIGHT + self.LINE_PADDING) * (i + 1))
                start = i * self.LINE_LENGTH
                finish = (i + 1) * self.LINE_LENGTH
                cr.show_text(self.description[start:finish])
        else:
            cr.move_to(self.x + self.CHAR_WIDTH,
                self.y + self.LINE_HEIGHT + self.LINE_PADDING)
            cr.show_text(self.description)

class DiagramCriterion(DiagramElement, Criterion):
    '''Defines a diagram criterion, which is represented as a red square.
    
    description: diagram criterion's description
    '''
    def __init__(self, description):
        DiagramElement.__init__(self)
        Criterion.__init__(self, description)
        self.color = (1.0, 0.0, 0.0)

class DiagramOption(DiagramElement, Option):
    '''Defines a diagram option, which is represented as a green square.
    
    description: diagram option's description
    '''
    def __init__(self, description):
        DiagramElement.__init__(self)
        Option.__init__(self, description)
        self.color = (0.0, 1.0, 0.0)

class DiagramQuestion(DiagramElement, Question):
    '''Defines a diagram question, which is represented as a blue square.
    
    description: diagram question's description
    '''
    def __init__(self, description):
        DiagramElement.__init__(self)
        Question.__init__(self, description)
        self.color = (0.0, 0.0, 1.0)

class Diagram(object):
    def __init__(self, drawingArea):
        '''Defines a diagram and it's drawing area.
        
        drawingArea: drawingArea widget
        '''
        self.drawingArea = drawingArea
        self.drawingArea.connect('expose-event', self.draw)
        
        self.elements = []
        self.relationships = []
        
        self.BG_COLOR = (1.0, 1.0, 1.0)
        self.WIDTH = 800
        self.HEIGHT = 600
    
    def draw(self, event=None, widget=None):
        '''Draws the diagram.'''
        cr = self.drawingArea.window.cairo_create()
        cr.set_source_rgb(self.BG_COLOR[0], self.BG_COLOR[1], self.BG_COLOR[2])
        cr.rectangle(0, 0, self.WIDTH, self.HEIGHT)
        cr.fill()
        
        for el in self.elements + self.relationships:
            el.draw(cr)
    
    def removeElement(self, el):
        '''Removes the currently selected element from the diagram. If there are
        any relationships with the currently selected element, they are removed
        as well.'''
        for el2 in self.elements:
            if isinstance(el2, Relational) and el2.hasRelationship(el) >= 0:
                r = el2.removeRelationship(el)
                del self.relationships[self.relationships.index(r)]
            elif isinstance(el, Relational) and el.hasRelationship(el2) >= 0:
                r = el.removeRelationship(el2)
                del self.relationships[self.relationships.index(r)]
        del self.elements[self.elements.index(el)]
        self.draw()
    
    def moveElement(self, el, direction):
        '''Moves the currently selected element.
        
        el: the element
        direction: direction to move (up, down, right, left)
        '''
        if direction == UP:
            el.y -= 5
        elif direction == DOWN:
            el.y += 5
        elif direction == RIGHT:
            el.x += 5
        elif direction == LEFT:
            el.x -= 5
        self.draw()
    
    def addElement(self, el, x, y):
        '''Adds an element to the diagram.
        
        el: the element
        x: x coordinate
        y: y coordinate
        '''
        el.setPosition(x, y)
        self.elements.append(el)
        self.draw()
    
    def addRelationship(self, elementA, elementB):
        '''Adds a directional relationship from the first to the second element.
        
        elementA: first element
        elementB: second element
        '''
        r = DiagramRelationship(elementA, elementB)
        self.relationships.append(r)
        self.draw()
    
    def selectElement(self, x, y):
        '''Selects an element at a given position. If there's no element,
        returns None, else returns the element.
        
        x: x coordinate
        y: y coordinate
        '''
        for el in self.elements:
            if el.hasPoint(x, y):
                return el
        return None

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
            self.INSERT_RELATIONSHIP: 'Select two elementos to insert a new Relationship. Press "Esc" to cancel.',
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
        '''Handles a left click event on the drawing area.'''
        if event.button != 1:
            return
        
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
            else:
                el = self.diagram.selectElement(event.x, event.y)
                if el:
                    try:
                        self.diagram.addRelationship(self.obj, el)
                    except RelationshipAlreadyExists:
                        print 'ja existe'
                    except RelationshipNotPossible:
                        print 'nao pode relacao'
                    self.setStatus(self.NOP)
    
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
