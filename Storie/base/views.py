from django.shortcuts import render
from .models import Story
from django.db.models import Q

# Create your views here.

def home(request):
    context = {
        'story': Story.objects.all()
    }
    return render (request, 'base/home.html' , context)

def home_latest(request):
    context = {
        'story': Story.objects.all().order_by('-date_posted')
    }
    return render (request, 'base/home_latest.html' , context)



def Read_story(request, pk):
    story = Story.objects.get(pk=pk)
    context = {
        'story': story
    }
    return render (request, 'base/read_story.html' , context)

def search(request):
    query = request.GET.get('q')
    if query:
        story = Story.objects.filter(Q (title__icontains=query) | Q (description__icontains=query))
        context = {'story': story, 'query': query}
    else:
        context = {}
    return render(request, 'base/search.html', context )


def Comment(request, pk):
    story = Story.objects.get(pk=pk)