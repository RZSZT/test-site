from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home, name="home"),
    path('ascii_gif', views.ascii_gif, name="ascii_gif"),
    path('ascii_image', views.ascii_image, name="ascii_image"),
    path('about', views.about, name="about"),
    path('process', views.process, name="process"),
    path('results', views.ascii_gif, name="results"),
    path('image_results', views.ascii_image, name="image_results"),
    ]
