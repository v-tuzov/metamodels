# -*- coding: utf-8 -*-

'''
    Команда создания БД по описанию.    
'''

from django.core.management.commands import syncdb
from django.core.management.base import BaseCommand, CommandError
from dynamic.factory import ModelsFactory


class Command(BaseCommand):
    args = '<filename>'
    help = 'Creates database for the given models description'

    def handle(self, *args, **options):
    
        mf = ModelsFactory()
        mf.load(args[0])    
        syncdb.Command().handle_noargs()
        self.stdout.write('OK')
       
                
        
        
