from django.contrib import admin
from django.urls import path
from library import views

urlpatterns = [
    path('', views.home, name='libraryhome'),
    path('uploadfile/', views.bookupload, name='newBook'),
    path('description/<str:description>', views.book_description, name='describebook'),
]
