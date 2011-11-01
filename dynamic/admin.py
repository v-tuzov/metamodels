from dynamic import models

try:
    models.load_models('/tmp/models.dump')
except IOError:
    pass 
 
