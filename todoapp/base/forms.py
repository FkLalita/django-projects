from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ('name','details')

