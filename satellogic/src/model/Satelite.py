'''
Created on 8 mar. 2018

@author: miglesias
'''

import time
from multiprocessing import Process
from termcolor import colored

class Satelite(object):
    
    def __init__(self, id):
        self.__id = id
        print colored("SATELITE {0} - Creado".format(self.__id), 'yellow')
    
    def __del__(self):
        print colored("SATELITE {0} - Destruido".format(self.__id), 'yellow')
    
    def do(self, conn):
        
        tasks = conn.recv()
        
        # Creamos la piscina (Pool)
        piscina = []

        for task in tasks:
            print colored("SATELITE {0} - Inicia tarea {1} (Duracion {2} segundos)".format(self.__id, task.name, task.payload), 'green')
            piscina.append(Process(name="Tarea {0}".format(task.name), target=task.do, args=(self.__id,)))
 
        # Arrancamos a todas las tareas
        print("SATELITE {0} : arrancando tareas".format(self.__id))
        for proceso in piscina:
            proceso.start()
         
        print("SATELITE {0} : esperando a que las tareas terminen".format(self.__id))
        # Mientras la piscina tenga procesos
        while piscina:
            # Para cada proceso de la piscina
            for proceso in piscina:
                # Revisamos si el proceso ha muerto
                if not proceso.is_alive():
                    # Recuperamos el proceso y lo sacamos de la piscina
                    proceso.join()
                    piscina.remove(proceso)
                    del(proceso)
            
            # Para no saturar, dormimos al satelite durante 1 segundo
            print("SATELITE {0} : esperando a que las tareas termine".format(self.__id))
            time.sleep(1)
         
        print("SATELITE {0} : todas laos tareas han terminado, cierro".format(self.__id))