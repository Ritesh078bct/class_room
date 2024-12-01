from django.shortcuts import render,redirect
from .models import Room,Topic,Message,User
from .forms import RoomForm,RegistrationForm,UserForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# from django.contrib.auth.models import User

from django.db.models import Q
# from django.http import HttpResponse
# Create your views here.

def index(request):
    rooms=Room.objects.all()
    topics=Topic.objects.all()
    messages=Message.objects.all()
    # for room in rooms:
    #     for participant in room.participants.all():
    #         print(participant)
    return render(request, 'base/index.html',{'rooms':rooms,'topics':topics,'messages':messages}) # This is the view function that will be called when the URL is visited. It will render the index.html template.

@login_required
def createRoom(request):
    form = RoomForm(request.POST)
    topics=Topic.objects.all()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('index')
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
            # new_topic_name = form.cleaned_data.get('new_topic')
            # if new_topic_name:
            #     # Create the new topic if it doesn't exist
            #     room.topic, created = Topic.objects.get_or_create(name=new_topic_name)
            # else:
            #     # Use the selected existing topic
            #     room.topic = form.cleaned_data.get('topic')
            # room.save()

    else:
        form=RoomForm()
    return render(request, 'base/create-room.html',{'form':form,'topics':topics})

@login_required
def updateRoom(request,room_id):
    topics=Topic.objects.all()
    # print(request)
    room = get_object_or_404(Room,pk=room_id,host=request.user)
    form=RoomForm(request.POST, instance=room)
    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic=topic
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect('index')
    else:
        form=RoomForm(instance=room)
    return render(request,'base/update-room.html',{'form':form,'topics':topics})

@login_required
def deleteRoom(request,room_id):
    room = get_object_or_404(Room,pk=room_id,host=request.user)
    if request.method == "POST":
        room.delete()
        return redirect('index')
    return render(request,'base/delete-room.html')


def registerUser(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('index')
    else:
        form=RegistrationForm()
    return render(request,'registration/register.html',{"form":form})







def search_feature(request):

    topics=Topic.objects.all()

    if request.method=="GET":
        q = request.GET.get('q') 
        rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
        return render(request, 'base/search-result.html', { 'rooms':rooms,'topics':topics})
    
    # Check if the request is a post request.
   
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        rooms = Room.objects.filter(name__contains=search_query)
        return render(request, 'base/search-result.html', {'query':search_query, 'rooms':rooms,'topics':topics})
    else:
        return render(request, 'base/search-result.html',{'topics':topics})
    


def room(request,room_id):
    room=get_object_or_404(Room, pk=room_id)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method == "POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            message=request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room',room_id=room_id)
    else:
        pass
    context={
        'room':room,
        'messages':room_messages,
        'participants':participants
        }
    return render(request,'base/room.html',context)




@login_required
def deleteMessage(request,message_id):
    message = get_object_or_404(Message,pk=message_id,user=request.user)
    if request.method == "POST":
        message.delete()
        return redirect('room',room_id=message.room.id)
    return render(request,'base/delete-message.html')


def userProfile(request,user_id):
    # user = User.objects.get(id=user_id)
    user=get_object_or_404(User,pk=user_id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    print(user)
    print(request.user)
    flag=None
    if user == request.user:
        flag="True"
        print(flag)
    context = {'feed_user': user, 'rooms': rooms,
               'messages': room_messages, 'topics': topics,'flag':flag}
    return render(request, 'base/profile.html', context)



@login_required
def updateProfile(request):
    user=request.user
    form=UserForm(instance=user)
    print(form)
    if request.method=="POST":
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',user_id=user.id)
    return render(request,"base/update-profile.html",{'form':form})