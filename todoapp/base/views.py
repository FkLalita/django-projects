from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def taskHome(request):
    q = request.GET.get('q')
    if  q != None:
        task = Task.objects.filter(name__icontains=q)
    else:
        task = Task.objects.all()

    context = {'task':task}
    return render (request, "base/task_home.html", context)

def home(request):
    if request.user.is_authenticated:
        task = Task.objects.filter(user_id=request.user.id)
    else:
        return redirect('task_home')
    context = {'task':task}
    return render (request, "base/home.html", context)



def taskView(request, pk):
    task = get_object_or_404(Task, pk=pk)
    context = {'task':task}
    return render (request, "base/task_view.html", context)

@login_required(login_url='loginpage')
def  taskCreate(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render (request, "base/task_create_update.html", {'form':form})


@login_required(login_url='loginpage')
def taskUpdate(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect ('home')
    else:
        form = TaskForm(instance=task)
    return render (request, "base/task_create_update.html", {'form':form, 'task':task})

@login_required(login_url='loginpage')
def taskDelete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect ('home')
    return render (request, "base/delete_task.html")


def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username == user.username.lower()
            user.save()
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'error occured')
    return render (request, "base/login_signup.html", {"form":form})


def loginpage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'error')

    return render (request, "base/login_signup.html", {'page':page})


def logoutuser(request):
    logout(request)
    return redirect('home')