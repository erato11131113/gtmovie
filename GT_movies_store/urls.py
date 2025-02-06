"""
URL configuration for GT_movies_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home import views as home_views  # Add this line
from movies import views as movie_views  # Add this line

print("Loading main URLs")  # Add this debug line

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_views.index, name='home'),  # Direct view reference
    path('movies/', movie_views.index, name='movies'),  # Direct view reference
]