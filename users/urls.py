from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.movies_login, name='movies_login'),
    path('logmeout', views.movies_logout, name='movies_logout'),
    path('register', views.register, name='register'),
]
