from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
   
    return render(request, 'home.html' )

# THIS FUNCTION ALLOWS US TO ADD USERS TO OUR DB THROUGH A LOGIN IN THE FRONT FRONT
def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
        
    } )
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                } ) 
                
               
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Password do not match'
                } ) 
                                                             # CRUD

# READ
# CON ESTE DECORADOR VAMOS A PROTEGER NUESTRAS RUTAS
@login_required
def tasks(request):
    """ esta consulta lo que hace es que filtra las tareas del usuario actualmente logueado """
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = False).order_by('datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

# CREATE
@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html',{'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form': TaskForm,
                'error': 'Please provide valida data'                                       
                })

#READ FOR ID AND UPDATE AT THE SAME TIME
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form': form, 'error': "Error updating task"})

#THIS FUNCTION ALLOWS US TO FILL THE DATE COMPLETED FIELD TO INDICATE THAT THE TASK HAS BEEN FINISHED
@login_required
def complete_task(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')     

#DELETE
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

#ESTA FUNCION NOS PERMITE CERRAR NUESTRA SESION
@login_required    
def signout(request):
    logout(request)
    return redirect('home')

#THIS FUNCTION ALLOWS US TO START SECTION WITH A USER ALREADY CREATED FROM THE FRONT
def signin(request):
    """ si el metodo es get usa el primer if """

    """ y si no es get significa que me estan enviando datos usa esto el else"""

    """ si el usuario es invalido devuelve un error ejecutando el segundo if """

    """ y si el usuario es valido redireccionalo a la vista tasks """

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')




   
    