'''
Created on 8 mar. 2018

@author: miglesias
'''

from satellogic import app
from satellogic.service.TaskScheduler import initialice_satelites, kernel, distribute_tasks
from satellogic.model.Task import Task

@app.route("/run")
def run():
    
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
    
    initialice_satelites(tasks_per_satelite, number_of_satelites, tasks)
    
    kernel(tasks_per_satelite, number_of_satelites, tasks)
    
    distribute_tasks(tasks_per_satelite, number_of_satelites)
    
    return "Successful run!"   
    
 
    