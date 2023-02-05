from django.shortcuts import render, redirect  
from forms import ContentForm   
from django.template import RequestContext


def Contents(request):
    return render(request, 'contents.html')  


def Create_Content(request):
    return render(request, 'create_content.html')  


def Create_Content_Insert(request):
    if request.method == "POST":  
        form = ContentForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/')  
            except:  
                pass  

    else:    
        form = ContentForm() 
    return render(request, 'create_content.html', {'form': form})  