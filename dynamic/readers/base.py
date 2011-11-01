# -*- coding: utf-8 -*-

"""Базовый класс, считывающих описание модели"""


from abc import ABCMeta, abstractmethod
from django.utils import simplejson
from xml.sax.xmlreader import XMLReader


# допустимые названия полей в текстовом описании модели (простая проверка синтаксиса)


TABLE_NAME = 'tbl_name'
TABLE_TITLE = 'title'
TABLE_FIELDS = 'fields' 

FIELD_NAME = 'id'
FIELD_TITLE = 'title'
FIELD_TYPE = 'type'

INT = 'int'
CHAR = 'char'
BOOL = 'bool'

TABLE_KEYS = (TABLE_NAME, TABLE_TITLE, TABLE_FIELDS)
FIELD_KEYS = (FIELD_NAME, FIELD_TITLE, FIELD_TYPE) 
FIELD_TYPES = (INT, CHAR, BOOL)


class TField(object):
    
    
    def __init__(self, name, title, type_):
        
        if not type_ in FIELD_TYPES:
            raise Exception('Undefined field type "%s"' % (type_))
        
        self.name = name
        self.title = title
        self.type = type_
        
        
    @classmethod
    def from_json(cls, json_field):
        
        return cls(json_field[FIELD_NAME],  json_field[FIELD_TITLE], json_field[FIELD_TYPE])
        
            
class TTable(object):
    
    
    def __init__(self, name, title, fields):
        
        self.name = name
        self.title = title
        self.fields = fields
        
        
    @classmethod
    def from_json(cls, json_table):
        
        fields = []
        for json_field in json_table[TABLE_FIELDS]:
            fields.append(TField.from_json(json_field))
            
        return cls(json_table[TABLE_NAME],  json_table[FIELD_TITLE], fields)    


class SyntaxError(Exception):
    
    
    def __init__(self, msg):
        self.parameter = msg
    
        
    def __str__(self):
    
        return repr('Models definition syntax error. %s'  % (self.parameter))    
        

class BaseReader(object):
    
    """
       Базовый класс ридера описания модели.
       Любой ридер должен возвращать результат чтения в формате json:
       
       [{"tbl_name": "table1", 
         "title": "title1", 
         "fields": [{"id": "id1",  "title": "title1",  "type": "char"},     
                   { "id": "id2",  "title": "title2", "type": "int"}] 
        },
        {"tbl_name": "table2", 
         "title": "title2", 
         "fields": [{"id": "id1","title": "title1", "type": "char"},     
                    {"id": "id2","title": "title2", "type": "bool"}] 
        }
       ] 
    """
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def loads(self, str):
        pass
    

    def load(self, filename):
        
        input_file = open(filename)
        str = input_file.read()
        input_file.close()
        return self.loads(str)
