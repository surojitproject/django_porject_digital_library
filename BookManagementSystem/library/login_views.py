from django.shortcuts import render, redirect, reverse
from .forms import Userform
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, UserTable
import os

# Create your views here.

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        form = Userform()
        if request.method == 'POST':
            form = Userform(request.POST)
            if form.is_valid():
                user_obj = form.save()
                user_profile = UserProfile(user=user_obj)
                user_profile.save()
                first_name = form.cleaned_data.get('first_name').title()
                username = form.cleaned_data.get('username')

                messages.success(request, f'😎 Hello {username or first_name}, your account was created succesfully! please login to continue.')
                return redirect('/accounts/login/')
        
        context = {
                'form':form
            }
        return render(request, 'library/signup.html', context)
    

def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, f'{request.user} you are already logged in')
        return redirect('/home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password )
        
            if user is not None:     
                login(request, user)
                name = request.user.get_full_name().title()
                if not name or name=='Unknown' or name=='Unknown Unknown':
                    name = request.user
                messages.success(request, f'Welcome {name}, You have sucessfully logged in!')
                return redirect('home')
            else:
                messages.info(request, '😥 Username or password is incorrect!')
                return redirect('/accounts/login/')
                
        return render(request, 'library/login.html', context = {})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Thanks for visiting Digital Library. See you soon! 🙂')
    return redirect('/')

@login_required
def update_user_profile(request):
    user = User.objects.get(id=request.user.id)
    fname = user.first_name;  lname = user.last_name; email = user.email; 
    nfname = request.POST['first_name']
    nlname = request.POST['last_name']
    nemail = request.POST['email']
    user_profile = UserProfile.objects.get(user_id=request.user.id)

    if request.method == 'POST':      
        if len(request.FILES) != 0:         
            if user_profile.profile_pic != 'uploads/img_avatar.png':
                if len(user_profile.profile_pic) > 0:
                    os.remove(user_profile.profile_pic.path)              
            user_profile.profile_pic = request.FILES['profile_pic'] or None           
        user_profile.save()
    
    if fname==nfname and lname==nlname and email==nemail and len(request.FILES) == 0:   
        messages.success(request, 'No update detected in your pofile!')
        return redirect(f"{request.POST['path']}")
    
    else:
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'You have successfully updated your pofile!')
        return redirect(f"{request.POST['path']}")
    

@login_required
def delete_user(request, id):
    user = User.objects.get(id=id)
    user_profile = UserProfile.objects.get(user_id=request.user.id)      
            
    if user_profile.profile_pic != 'uploads/img_avatar.png':
        if len(user_profile.profile_pic) > 0:
            os.remove(user_profile.profile_pic.path)

    user.delete()
    messages.success(request, 'Your account successfully deleted!')
    return redirect('/home')
