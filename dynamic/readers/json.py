# -*- coding: utf-8 -*-

from base import BaseReader
from base import TABLE_FIELDS, TABLE_KEYS,FIELD_TYPE, FIELD_TYPES, FIELD_KEYS
from django.utils import simplejson


class Reader(BaseReader):
    
    """Ридер, считывающий модели из Json структуры"""
    
    def loads(self, str):
        try:
            text_models = simplejson.loads(str)
        except ValueError:
            raise SyntaxError('Json syntax error')
        
        # Очень упрощённый лексический анализ
        for text_model in text_models:
            for key, val in text_model.items():
                if not key in TABLE_KEYS:
                    raise SyntaxError('Undefined model definition field "%s"' % (key)) 
                if key == TABLE_FIELDS:
                    for field in val:
                        for fkey, fval in field.items():
                            if fkey not in FIELD_KEYS:
                                raise SyntaxError('Undefined model field definition key "%s"' % (fkey))
                            if fkey == FIELD_TYPE:
                                if not fval in FIELD_TYPES:
                                    raise SyntaxError('Undefined model field type "%s"' % (fval))
                    
        return text_models