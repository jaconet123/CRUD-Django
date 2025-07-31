from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import createtaskform
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                createduser = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                createduser.save()
                login(request, createduser)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exist'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })

@login_required
def logoutx(request):
    logout(request)
    return redirect('home')

@login_required
def tasks(request):
    task_list = Task.objects.filter(
        user=request.user, completiondate__isnull=True)
    return render(request, 'tasks.html', {
        'tasklist': task_list
    })
@login_required    
def completed_tasks(request):
    task_list = Task.objects.filter(
        user=request.user, completiondate__isnull=False).order_by('-completiondate')
    return render(request, 'tasks.html', {
        'tasklist': task_list
    })



def loginx(request):
    if request.method == 'GET':
        return render(request, 'loginx.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginx.html', {
                'form': AuthenticationForm,
                'error': 'wrong credentials'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required    
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': createtaskform

        })
    else:
        try:
            form = createtaskform(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'from': createtaskform,
                'error': 'Missing data/not valid data'

            })

@login_required    
def task_detail(request, task_id):

    if request.method == 'GET':
        task_selected = get_object_or_404(Task, pk=task_id, user=request.user)
        detailform = createtaskform(instance=task_selected)
        return render(request, 'task_detail.html', {
            'task': task_selected,
            'form': detailform
        })
    else:
        try:
            task_selected = get_object_or_404(
                Task, pk=task_id, user=request.user)
            form = createtaskform(request.POST, instance=task_selected)
            form.save()
            return redirect(tasks)
        except ValueError:
            task_selected = get_object_or_404(Task, pk=task_id)
            detailform = createtaskform(instance=task_selected)
            return render(request, 'task_detail.html', {
                'task': task_selected,
                'form': detailform,
                'error': "error updating task"
            })

@login_required    
def complete_task(request,task_id):
    task_selected = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task_selected.completiondate= timezone.now()
        task_selected.save()
        return redirect (tasks)
    
@login_required    
def delete_task(request,task_id):
    task_selected = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task_selected.delete()
        return redirect (tasks)
