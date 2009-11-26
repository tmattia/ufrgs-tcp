#!/usr/bin/env python
#-*- coding:utf-8 -*-

class RelationshipAlreadyExists(Exception):
    '''Exception signalizing that a relationship from the first to the second
    element already exists.'''
    pass

class RelationshipDoesNotExist(Exception):
    '''Exception signalizing that a relationship from the first to the second
    element does not exist.'''
    pass

class RelationshipNotPossible(Exception):
    '''Exception signalizing that a relationship between two elements is not
    possible due to restrictions in the first element.'''
    pass

class Relational(object):
    def __init__(self, relates_to = ()):
        '''Defines a Relational object.
        
        relates_to: list of class references with acceptable relationships
        '''
        self._relationships = []
        self._relates_to = relates_to
    
    def addRelationship(self, element, pro=True):
        '''Adds a relationship to a given element.
        
        If a relationship already exists, raises a RelationshipAlreadyExists
        exception.
        
        If a relationship cannot be established between the two elements, raises
        a RelationshipNotPossible exception.
        
        element: second element
        pro: boolean defining if first element favors second element or not
        '''
        if isinstance(element, self._relates_to):
            r = Relationship(self, element, pro)
            if r in self._relationships:
                raise RelationshipAlreadyExists
            else:
                self._relationships.append(r)
        else:
            raise RelationshipNotPossible
    
    def hasRelationship(self, element):
        '''Returns a boolean idicating if there is a relationship to another
        element.
        
        element: the other element
        '''
        r = Relationship(self, element)
        try:
            index = self._relationships.index(r)
            return index
        except ValueError:
            return -1
    
    def removeRelationship(self, element):
        '''Removes a relationship to another element, if it exists.
        
        element: the other element
        '''
        index = self.hasRelationship(element)
        if index >= 0:
            return self._relationships.pop(index)
        return None
    
    def favors(self, element):
        '''If there is a relationship to another element, returns a boolean
        indicating if it is pro or against.
        
        If the relationship does not exists, raises a RelationshipDoesNotExist
        exception.
        
        element: the other element
        '''
        index = self.hasRelationship(element)
        if index >= 0:
            return self._relationships[index].pro
        else:
            raise RelationshipDoesNotExist
        

class Relationship(object):
    def __init__(self, elementA, elementB, pro=True):
        '''Defines a directional relationship from the first to the second
        element.
        
        elementA: first element
        elementB: second element
        pro: boolean defining if first element favors second element or not
        '''
        self.elementA = elementA
        self.elementB = elementB
        self.pro = pro
    
    def __eq__(self, other):
        '''Compares equality between relationships.
        
        Returns True if both relationships have the same elements, in the same
        order, or False otherwise.'''
        return (self.elementA == other.elementA) \
            and (self.elementB == other.elementB)

class Element(object):
    def __init__(self, description):
        '''Defines an element.
        
        description: element's description
        '''
        self.description = description

class Criterion(Element):
    def __init__(self, description):
        '''Defines a criterion.
        
        description: criterion's description
        '''
        Element.__init__(self, description)

class Option(Element, Relational):
    def __init__(self, description):
        '''Defines an option.
        
        description: option's description
        '''
        Element.__init__(self, description)
        Relational.__init__(self, (Question, Criterion))

class Question(Element, Relational):
    def __init__(self, description):
        '''Defines a question.
        
        description: question's description
        '''
        Element.__init__(self, description)
        Relational.__init__(self, (Option, Criterion))


if __name__ == '__main__':
    '''If the script is run directly through a command line (e.g.
    `python qoc.py`), it runs the tests defined in "tests_qoc.txt"'''
    import doctest
    doctest.testfile('tests_qoc.txt', optionflags=doctest.NORMALIZE_WHITESPACE)
