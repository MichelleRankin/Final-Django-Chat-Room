from django.shortcuts import render, redirect
from chat.models import Room, Message, Customer
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerForm, CreateUserForm, UpdateUserForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='')
def room(request, room):
    username = request.user
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.user.username


    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(reversed(messages.values()))})




def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)





def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='User')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
        

    context = {'form':form}
    return render(request, 'register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')
    
# @login_required(login_url="login")
# def delete(request, id):
#     # check if message belongs to user
#     message = Message.objects.get(id=id)
#     if message.username == request.user or request.user.is_superuser:
#         message.delete()
#     # remove it from the database
#     # redirect back to same page
#     return redirect('delete')


@login_required(login_url='')
def updateprofile(request):
    # profile = Customer.objects.get(name=user)
    form = UpdateUserForm()
    if request.method == "POST":
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            customer_name = request.user.username
            userprofile = Customer.objects.get(name=customer_name)
            # profile.name = form.cleaned_data['name']
            userprofile.phone = form.cleaned_data['phone']
            userprofile.email = form.cleaned_data['email']
            userprofile.profile_pic = form.cleaned_data['profile_pic']
            userprofile.save()
            return redirect('profile')
    context = {"form":form}
    return render(request, 'updateprofile.html', context)

@login_required(login_url='')
def profile(request):
    user=request.user.username
    current = Customer.objects.get(name=user)
    return render(request, "profile.html", {"current":current})