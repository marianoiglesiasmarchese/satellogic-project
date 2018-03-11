'''
Created on 8 mar. 2018

@author: miglesias
'''

import time
from termcolor import colored

class Task(object):

    def __init__(self, name, payload, resource):
        self.name = name
        self.payload = payload
        self.resource = resource
        self.satelite_id = None
        print colored("TAREA {0} - Creada".format(self.name), 'yellow')
        
    def __del__(self):
        print colored("TAREA {0} - Destruido".format(self.name), 'yellow')        
    
    def do(self, satelite_id):
        time.sleep(self.payload)
        print colored("SATELITE {0} - fin de TAREA {1}".format(satelite_id, self.name), 'red')