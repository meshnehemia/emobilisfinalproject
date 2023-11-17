from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='intertainmenthome'),
    path('search/', views.get_youtube_data, name='search'),
]
