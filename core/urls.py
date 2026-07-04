from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='index'),  # This defines 'home' URL name
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
