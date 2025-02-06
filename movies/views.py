# movies/views.py
from django.shortcuts import render

def index(request):
    print("Movies index view called")
    
    return render(request, 'movies_index.html')
    
