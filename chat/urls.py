
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('logged-in/', views.home, name='home'),
    path('profile/', views.profile, name="profile" ),
    path('update/', views.updateprofile, name='updateprofile'),
    path('<str:room>/', views.room, name='room'),
    path('logged-in/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]
