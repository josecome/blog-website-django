from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django import forms
from .utilities import app_notifications
from django.contrib.auth.models import User
from contents.models import Posts as Post, Likes as Like, Comments as Comment
from django.db import connections
from django.http import HttpResponse
from django.core import serializers
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
import json


def loginPage(request):
    if request.user.is_authenticated:
        messages.success(request, _('AAAA'))
        return redirect('/')
    else:    
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                messages.success(request, _('Successfull logged in'))
                return redirect('/')           
            else:
                # Return an 'invalid login' error message.
                messages.info(request, _('Please, fill form'))
            
    return render(request, 'login.html')
    

# @login_required(login_url='login.html')    
def Blogs(request):    
    return render(request, 'home.html')  


def PostList(request):    
    Contents_list = Post.objects.all()
    data = serializers.serialize('json', Contents_list)
    #print('id: ' + str(Post.objects.all()[:1].get()))
    return HttpResponse(data, content_type="application/json")


def PageOfPostByUser(request, username):
    return render(request, 'posts.html')

def PostbyUser(request, username):
    user_id = int(User.objects.get(username=username).pk)    
    Contents_list = Post.objects.filter(user_id=user_id)
    data = serializers.serialize('json', Contents_list)
    return HttpResponse(data, content_type="application/json")


def getUserAtrib(request):
    array_data = ''
    aa = request.GET['ids']
    print(aa)
    ArrayOfIds = request.GET['ids'].split(',')
    data = User.objects.filter(pk__in=ArrayOfIds)
    for d in data:
        array_data += str(d.pk) + ":" + str(d.username) + ";"
      
    return HttpResponse(array_data)    


def PostLikes(request):
    data = Like.objects.all().values('post_id').annotate(total=Count('post_id')).order_by('total')
    array_data = ''
    for d in data:
        array_data += str(d['post_id']) + ":" + str(d['total']) + ";"
        
    return HttpResponse(array_data)


def PostComments(request):
    data = Comment.objects.all().values('post_id').annotate(total=Count('post_id')).order_by('total')
    array_data = ''
    for d in data:
        array_data += str(d['post_id']) + ":" + str(d['total']) + ";"
        
    return HttpResponse(array_data)


def addRemoveLike(request):
    print('==========begin==========')
    data = json.loads(request.body.decode())
    print('p: ' + str(data))
    res_data = {'result': 'added'} #If not liked before
    val_type_of_like = 'test' #request.POST['type_of_like']
    val_post_liked_link = 'test'
    val_date_created = datetime.now()
    val_date_updated = datetime.now()
    val_post_id = data['post_id']
    val_user_id = 1 #request.user.id
    new_like = Like.objects.create(type_of_like = val_type_of_like, post_liked_link = val_post_liked_link, 
                                date_created = val_date_created, date_updated = val_date_updated, 
                                post_id = val_post_id, user_id = val_user_id)

    if False:
        res_data = {'result': 'removed'} #If liked before

    return HttpResponse(res_data)


def addComment(request):
    print('==========begin==========')
    data = json.loads(request.body.decode())
    print('p: ' + str(data))
    res_data = {'result': 'added'} #If not liked before
    val_post_commented_link = 'test'
    val_date_created = datetime.now()
    val_date_updated = datetime.now()
    val_post_id = data['post_id']
    val_txt = data['txt']
    val_user_id = 1 #request.user.id
    new_comment = Comment.objects.create(post_commented_link = val_post_commented_link, 
                                date_created = val_date_created, date_updated = val_date_updated, 
                                post_id = val_post_id, user_id = val_user_id, comment = val_txt)

    if False:
        res_data = {'result': 'removed'} #If liked before

    return HttpResponse(res_data)


def Content(request, lnk):      
    #page_content = Contents.objects.get(id=id)
    page_content = Post.objects.get(link=lnk)
    return render(request, 'content.html', {'page_content': page_content})      


def registrationPage(request):
    form = CreateUserForm()
        
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.sucess(request, 'Account was sucessfully created for ' + user)      
            app_notifications.send_email(request)
            
            return redirect('login.html')
                                
    context = {'form': form}
    return render(request, 'register.html', context)
   
   
def logout_view(request):
    logout(request)
        
    return render(request,'logout.html')    