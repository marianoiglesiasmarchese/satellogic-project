import time
from multiprocessing import Process, Pipe
from satellogic.model.Task import Task
from satellogic.model.Satelite import Satelite
from termcolor import colored
 
'''
 
# Creamos la lista de tareas
tasks = []
tasks.append(Task('tarea1', 0, []))
tasks.append(Task('tarea2', 1, []))
tasks.append(Task('tarea3', 2, []))
tasks.append(Task('tarea4', 3, [1]))
tasks.append(Task('tarea5', 4, [2,1]))
tasks.append(Task('tarea6', 5, [3,2]))
tasks.append(Task('tarea7', 6, [4,3]))
tasks.append(Task('tarea8', 7, [5,4]))
tasks.append(Task('tarea9', 8, [6,5]))
tasks.append(Task('tarea10', 9, [7,6]))

# Ordeno las tareas de mayor a menor payload
tasks.sort(key=lambda task: task.payload, reverse=True)

for task in tasks:
    print(task.name + ' - {0}'.format(task.payload))



# Numero de satelites
number_of_satelites = 3

# Creamos la lista de tareas por cada satelite
tasks_per_satelite = []

'''

def initialice_satelites(tasks_per_satelite, number_of_satelites, tasks):
    # Creo la lista de tareas que debe resolver cada satelite y garantizo que cada uno tenga al menos una tarea con payload alto.
    for i in range(0, number_of_satelites):
        tasks_per_satelite.append([])
        if len(tasks) > 0:
            tasks_per_satelite[i].append(tasks.pop(0))



# Valido si se puede incluir la tarea en la lista de tareas del satelite
def canInclude(tasks, new_task):
    for task in tasks:            
        if len(set(new_task.resource).intersection(task.resource)) > 0:
            return False
    return True    

def kernel(tasks_per_satelite, number_of_satelites, tasks):
    # Por cada satelite, agrego las tareas que puede resolver en base los recursos que se necesitan
    last_size = 0
    while len(tasks) > 0 and last_size != len(tasks):
        last_size = len(tasks)
        for i in range(0, number_of_satelites):
            j = 0
            end = False
            while j < len(tasks) and not end:
                if canInclude(tasks_per_satelite[i], tasks[j]):
                    tasks_per_satelite[i].append(tasks.pop(j))
                    end = True
                j = j + 1
        
    for i in range(0, number_of_satelites):
        print( 'Satelite {0} -> '.format(i))
        for task in tasks_per_satelite[i]:
            print(task.name + ' - {0}'.format(task.payload))
        
        
        
def distribute_tasks(tasks_per_satelite, number_of_satelites):
    # Creamos una lista de colas 
    pipes = []
    
    # Creamos la piscina de procesos (Pool)
    piscina = []
    for i in range(0, number_of_satelites):
        print("ESTACION TERRENA: creo un pipe entre la estacion terrena y el SATELITE {0}".format(i))    
        parent_conn, child_conn = Pipe()
        pipes.append(parent_conn)
        print("ESTACION TERRENA: comparto las tareas del SATELITE {0}".format(i))
        parent_conn.send(tasks_per_satelite[i])
        print("ESTACION TERRENA: creando SATELITE {0}".format(i))
        piscina.append(Process(name="Satelite {0}".format(i), target=Satelite(i).do, args=(child_conn,)))
    
     
    # Arrancamos a todos los procesos
    print("ESTACION TERRENA: arrancando satelites")
    for proceso in piscina:
        proceso.start()
     
    print("ESTACION TERRENA: esperando a que los satelites resuelvan las tareas asignadas")
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
        
        # Para no saturar, dormimos la estacion terrena durante 1 segundo
        print("ESTACION TERRENA: esperando a que los satelites resuelvan las tareas asignadas")
        time.sleep(1)
     
    print("ESTACION TERRENA: todos los satelites han terminado, cierro")
    
    # recibo todas las tareas que no pudieron terminarse
    for i in range(0, len(pipes)):
        incompleted_tasks = pipes[i].recv()
        if len(incompleted_tasks) > 0:
            for task in incompleted_tasks:
                print colored('SATELITE {0} no pudo terminar tarea {1}'.format(i, task.name), 'red')
    

