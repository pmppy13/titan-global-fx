from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('platforms/', views.PlatformsView.as_view(), name='platforms'),
    path('markets/', views.MarketsView.as_view(), name='markets'),
    path('plans/', views.PlansView.as_view(), name='plans'),
]