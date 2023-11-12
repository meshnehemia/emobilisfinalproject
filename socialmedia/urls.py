from django.contrib import admin
from django.urls import path
from socialmedia import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginPage,name='login'),
     path('register/',views.registerPage,name='register'),
    path('logout/',views.logoutUser,name='logout'),
    path('navbar/',views.navbar,name='navbar'),
    path('room/<str:pk>/',views.room, name='room'),
    path('profile/<str:pk>/',views.userProfile, name='user-profile'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>',views.deleteMessage,name='delete-message'),
    path('update-user/',views.updateUser,name='update-user'),
    path('topics/',views.topicsPage,name='topics'),
]
