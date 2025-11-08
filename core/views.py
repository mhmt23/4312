from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileSkillUpdateForm, ServiceCreationForm
from .models import UserProfile, Service
from django.contrib.auth.decorators import login_required

def home_view(request):
    services = Service.objects.filter(status='open').order_by('-created_at')
    return render(request, 'home.html', {'services': services})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user) # Use get_or_create to be safe
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileSkillUpdateForm(request.POST)
        if form.is_valid():
            selected_skills = form.cleaned_data['skills']
            profile.skills.set(selected_skills)
            return redirect('profile')
    else:
        initial_skills = profile.skills.all()
        form = ProfileSkillUpdateForm(initial={'skills': initial_skills})

    return render(request, 'profile.html', {
        'form': form,
        'profile': profile
    })

@login_required
def create_service_view(request):
    if request.method == 'POST':
        form = ServiceCreationForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.creator = request.user
            service.save()
            return redirect('home') # Redirect to home to see the new service
    else:
        form = ServiceCreationForm()
    return render(request, 'create_service.html', {'form': form})
