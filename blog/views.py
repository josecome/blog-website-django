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
from django.contrib.auth.models import User
from contents.models import (
    Post,
    Comment,
    Like,
    Share,
)
from django.db import connections
from django.http import HttpResponse
from django.core import serializers
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
import json
from django.db.models import Q
from .utils import (
    send_email,
    send_activation_email, 
    send_reset_password_email, 
    send_forgotten_username_email, 
    send_activation_change_email,
)
from .decorators import editor_required, user_is_post_author

def loginPage(request):
    if request.user.is_authenticated:
        messages.success(request, _('AAAA'))
        return redirect('/')
    else:    
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]
            # admin, password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                messages.success(request, _('Successfull logged in'))
                return redirect('/')           
            else:
                # Return an 'invalid login' error message.
                messages.info(request, _('Please, Invalid Username and Password!'))
            
    return render(request, 'login.html')
    

# @login_required(login_url='login.html')    
def Blogs(request):
    context = {}
    Post_list = Post.objects.all().order_by('id').select_related('user').annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )
    context['posts'] = Post_list

    return render(request, 'home.html', context)  


def PageOfPostByUser(request, username):
    context = {}
    Post_list = Post.objects.filter(user__username=username).select_related('user').order_by('id').select_related('user').annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )
    context['posts'] = Post_list
    context['user_posts'] = f'{Post_list[0].user.first_name} {Post_list[0].user.last_name}'
    
    return render(request, 'posts.html', context)


def getPostPage(request, link):
    context = {}
    Post_list = Post.objects.filter(link=link).select_related('user').order_by('id').select_related('user').annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )
    context['posts'] = Post_list
    context['user_posts'] = f'{Post_list[0].user.first_name} {Post_list[0].user.last_name}'
    context['link'] = link
    
    return render(request, 'post.html', context)


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
            send_email(request)
            
            return redirect('login.html')
                                
    context = {'form': form}
    return render(request, 'register.html', context)


@editor_required
def add_super_content():
    # This content is set by Editors
    pass

@user_is_post_author
def edit_post(request, user_id):
    # Only the author can edit the post
    pass

   
def logout_view(request):
    logout(request)
        
    return render(request,'logout.html')    