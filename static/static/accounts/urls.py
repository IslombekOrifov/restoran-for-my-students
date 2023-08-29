from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login_func, name='login'),
    
]