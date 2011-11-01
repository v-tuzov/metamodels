# -*- coding: utf-8 -*-

"""Фабрика моделей"""

from django.db import models
from django.contrib import admin
from django.utils.importlib import import_module
from dynamic.readers.base import INT, CHAR, BOOL
from dynamic.readers.base import TTable
from django.db import connection


def int_to_django(title):
    return models.IntegerField(verbose_name=title)


def char_to_django(title):
    return models.CharField(verbose_name=title, max_length=255)


def bool_to_django(title):
    return models.BooleanField(verbose_name=title)


# Преобразование типов полеq
FIELDS_MAPPING = {INT: int_to_django,
                  CHAR: char_to_django,
                  BOOL: bool_to_django}


class ModelsFactory(object):

    def __init__(self, reader='json'):
        
        reader_module = import_module('dynamic.readers.%s' % (reader))
        self.__reader = getattr(reader_module, 'Reader')()
         

    def load(self, filename):
        
        json_structure = self.__reader.load(filename) 
        return self.db_from_json(json_structure)
    
    
    def clear_db(self):
        # !Note! Сработает только  для Mysql -бакенда
        
        cursor = connection.cursor()
        cursor.execute('SHOW TABLES;') 
        tables = cursor.fetchall()
        for_deletion = [ (tbl[0]) for tbl in tables if  tbl[0].find('dynamic_') > -1]
        for table in for_deletion:
            sql = "DROP TABLE IF EXISTS %s;"  % (table)
            cursor.execute(sql)
    
    
    def loads(self, str):
        
        json_structure = self.__reader.loads(str)
        return self.db_from_json(json_structure)
    
        
    def db_from_json(self, json_structure):
        
        tables = []
        for json_table in json_structure:
            tables.append(TTable.from_json(json_table))
            
        django_models = []
        for table in tables:
            fields = {}
            for field in table.fields:
                fields[field.name] = FIELDS_MAPPING[field.type](field.title)
            django_models.append(self.create_model(table.name, table.title, fields))
            
        return django_models         
         
    def create_model(self, name, title, fields=None):
       
        class Meta:
            pass
        
        setattr(Meta, 'app_label', 'dynamic')
        attrs = {'__module__': 'dynamic.models', 'Meta': Meta}
        if fields:
            attrs.update(fields)
        model = type(name, (models.Model,), attrs)
        try:
            admin.site.register(model)
        except:
            pass
    
        return model
