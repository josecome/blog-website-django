from django.contrib import admin
from django.urls import path
from contents import views

urlpatterns = [
    path('', views.Contents, name="contents"),   
    path('create_content', views.Create_Content, name="create_content"),
    path('create_content_add/', views.Create_Content_Insert, name="create_content_add"),
]