from django.shortcuts import render


# Create your views here.
def Contents(request):
    return render(request, 'contents.html')  