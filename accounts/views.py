from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic import FormView, CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm
from core.models import TermsAndConditions



class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms'] = TermsAndConditions.objects.filter(is_active=True).first()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard:index')
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return redirect(self.success_url)
        messages.error(self.request, 'Invalid username or password.')
        return self.form_invalid(form)

def logout_view(request):
    logout(request)
    return redirect('core:home')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms'] = TermsAndConditions.objects.filter(is_active=True).first()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard:index')  # Default
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            
            # ===== CHECK: If user is admin, redirect to admin dashboard =====
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard:index')
            
            return redirect(self.success_url)
        messages.error(self.request, 'Invalid username or password.')
        return self.form_invalid(form)

def logout_view(request):
    logout(request)
    return redirect('core:home')    