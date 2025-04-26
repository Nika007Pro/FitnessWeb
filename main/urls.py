from django.urls import path, include
from .views import home, coach, register, handlelogin, handlelogout, profile, update, team_members, stat
from . import views
from .views import update_profile, membership_view

urlpatterns = [
    path('home', home, name='home'),
    path('trainers', views.coach, name='trainers'),
    path('', home, name='home'),
    path('coach', coach, name='coach'),
    path('register', register, name='register'),
    path('login', handlelogin, name='auth'),
    path('logout', handlelogout, name='exit'),
    path('profile', profile, name='profile'),
    path('update', update, name='update'),
    path('stat/', stat, name='stat'),
    path('team_members', team_members, name='team_members'),
    path('price/', views.price_view, name='price'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('update_profile/', update_profile, name='update_profile'),
    path('card/', membership_view, name='membership_view'),
]
