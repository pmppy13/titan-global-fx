from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('platforms/', views.platforms_view, name='platforms'),
    path('markets/', views.markets_view, name='markets'),
    path('analysis/', views.analysis_view, name='analysis'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]
