from django.contrib import admin
from django.urls import path
from contents import views

urlpatterns = [
    path('', views.Contents, name="contents"),   
    path('create_content/', views.Create_Content, name="create_content"),
]