from django.shortcuts import render, redirect  
from .forms import ContentForm   
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import datetime


def Contents(request):
    return render(request, 'contents.html')  


def Create_Content(request):     
    form = ContentForm() 
    return render(request, 'create_content.html', {'form': form})  


def Content(request, id):
    page_content = Content.get(id=id)
    return render(request, 'create_content.html', {'page_content': page_content})      


def Create_Content_Insert(request):
    if request.method == "POST":  
        form = ContentForm(request.POST)  
        if form.is_valid():  
            try:  
                form = form.save(commit=False)
                form.author = request.user
                form.date_created = datetime.datetime.now()
                form.date_updated = datetime.datetime.now()
                form.save()  
                messages.success(request, _('Successfull logged in'))
                return redirect('/contents/create_content')  
            except Exception as e:  
                pass

        else:    
            form = ContentForm() 
            messages.info(request, _('Please, fill form'))
            return render(request, 'create_content.html', {'form': form})  

    messages.info(request, _('Something happen'))
    return redirect('/')          