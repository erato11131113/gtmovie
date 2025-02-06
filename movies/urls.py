from django.urls import path
from . import views

print("Loading movies URLs")
urlpatterns = [
    path('', views.index, name='index')
]
