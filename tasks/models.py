
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    """ (blank=True):significa que si le pasan nada por defecto va a estar vacio """
    description = models.TextField(blank=True)
    """ (auto_now_add=True): significa que a la hora de que creemos una tarea y no le coloquemos la fecha este comando lo creara automaticamente """
    created = models.DateTimeField(auto_now_add=True)
    """ (null=True):con este comando tenemos que poner la fecha manualmente cuando se complete una tarea """
    datecompleted = models.DateTimeField(null=True,blank=True)
    """ (default=False):este comando quiere decir que cuando se cree una tarea no todas van hacer importantes, habria que ponerlas en true para que sean important """
    important = models.BooleanField(default=False)
    """ (on_delete=models.CASCADE): este comando nos va a permitir que a la hora que se elimine un usuario por defecto tambien se eliminen las tareas que estan relacionadas a este """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__ (self):
        return self.title +' - by '+ self.user.username
