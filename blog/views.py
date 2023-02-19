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
from contents.models import Content as Contents
from django.db import connections

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:    
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
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
    Contents_list = Contents.objects.all() 
    return render(request, 'home.html', {'contents': Contents_list})  


def Content(request, id):
    cursor = connections['default'].cursor()
    ss = "It is a markup language used to build web pages. HTML is an English acronym that means Hypertext Markup Language or in Portuguese Hypertext Markup Language. This is not a programming language but a markup language that contains a set of tags.\n\rIt was initially created to easily share documents in a research area at the European Council for Nuclear Research in Switzerland. In this language, codes (tags) delimit specific contents, according to their own syntax. HTML is designed to create web pages, when another programming resource is not included, the page created by it becomes static.\n\rNowadays it is easy to learn how to create a simple web page, since over the years the code involved and the demands of the market have made this work quite complex. To make the pages created through dynamic html it is necessary to add other languages like css, javascripts and others like: php, java, vb.net, c#, etc."
    tt = "HTML 5"
    cursor.execute("update contents set body = %s where topic = %s", [ss, tt])
    
    page_content = Contents.objects.get(id=id)
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