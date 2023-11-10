from django.shortcuts import render ,redirect
from django.db.models import Q
from .models import Room,Topic
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from  .forms import RoomForm
from django.contrib.auth.models import User
# Create your views here.

# rooms =[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'design with me'},
#     {'id':3,'name':'fronted developer'},
# ]
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username =request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user =User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')
        user =authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username and password does not match')
    context={'page':page}
    return render(request,'socialmedia/login_register.html',context)


def logoutUser(request):
        logout(request)
        return redirect('home')
    
    
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.username =user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Error occurred during registration")

    
    
    return render(request,'socialmedia/login_register.html',{'form':form})
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms =Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains =q)   |
        Q(description__icontains =q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'socialmedia/home.html', context )
def room(request,pk):
    rooms =Room.objects.get(id=pk)
    context = {'rooms':rooms}
    return render(request,'socialmedia/room.html' ,context)



@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method =='POST':
        form =RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context ={'form':form}
    return render(request,'socialmedia/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    if request.user != room.host:
        return HttpResponse("you are not allowed to use this site")
    
    if request.method == 'POST':
        form =RoomForm(request.POST,instance= room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context ={'form':form}
    return render(request,'socialmedia/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request ,pk):
    room =Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'socialmedia/delete.html',{'obj':room})

def navbar(request):
    return render(request,'navbar.html')