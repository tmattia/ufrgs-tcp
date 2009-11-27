#!/usr/bin/env python
#-*- coding:utf-8 -*-

from qoc import *
from keyboard_codes import *
import cairo

class DiagramRelationship(Relationship):
    def __init__(self, elementA, elementB, pro=True):
        '''Defines a directional diagram relationship from the first to the
        second element.
        
        elementA: first element
        elementB: second element'''
        elementA.addRelationship(elementB, pro)
        Relationship.__init__(self, elementA, elementB, pro)
        if self.pro:
            self.color = (0.6, 0.6, 0.6)
        else:
            self.color = (0.2, 0.2, 0.2)
    
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
    
    def addRelationship(self, elementA, elementB, pro):
        '''Adds a directional relationship from the first to the second element.
        
        elementA: first element
        elementB: second element
        '''
        r = DiagramRelationship(elementA, elementB, pro)
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
