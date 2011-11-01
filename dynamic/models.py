from dynamic.factory import ModelsFactory
from django.core.management.commands import syncdb


def load_models(filename):
                 
    mf = ModelsFactory()
    mf.clear_db()
    mf.load(filename)
    syncdb.Command().handle_noargs()
    



    

