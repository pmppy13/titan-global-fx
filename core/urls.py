from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home page
    path('', views.home_view, name='index'),
    
    # Static pages
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # Authentication pages (if using core views)
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    
    # Section anchors for single-page navigation
    # These are handled by the index page with # anchors
    # No separate URLs needed for #home, #about, #platforms, etc.
]
