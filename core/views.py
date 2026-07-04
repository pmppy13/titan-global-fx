from django.shortcuts import render

def home_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def platforms_view(request):
    return render(request, 'platforms.html')

def markets_view(request):
    return render(request, 'markets.html')

def analysis_view(request):
    return render(request, 'analysis.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')
