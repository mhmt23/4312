from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileSkillUpdateForm, ServiceCreationForm
from .models import UserProfile, Service
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib import messages

def home_view(request):
    services = Service.objects.filter(status='open').order_by('-created_at')
    return render(request, 'home.html', {'services': services})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, defaults={'time_credit': 10}) # Give starting credits
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
    created_services = Service.objects.filter(creator=request.user).order_by('-created_at')
    assigned_services = Service.objects.filter(assignee=request.user).order_by('-created_at')
    context = {'created_services': created_services, 'assigned_services': assigned_services}
    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileSkillUpdateForm(request.POST)
        if form.is_valid():
            profile.skills.set(form.cleaned_data['skills'])
            return redirect('profile')
    else:
        form = ProfileSkillUpdateForm(initial={'skills': profile.skills.all()})
    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def create_service_view(request):
    if request.method == 'POST':
        form = ServiceCreationForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.creator = request.user
            service.save()
            return redirect('home')
    else:
        form = ServiceCreationForm()
    return render(request, 'create_service.html', {'form': form})

def service_detail_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service_detail.html', {'service': service})

@login_required
@require_POST
def accept_service_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if service.status == 'open' and service.creator != request.user:
        service.status = 'in_progress'
        service.assignee = request.user
        service.save()
    return redirect('dashboard')

@login_required
@require_POST
def complete_service_view(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if service.creator == request.user and service.status == 'in_progress' and service.assignee is not None:
        try:
            with transaction.atomic():
                creator_profile = service.creator.userprofile
                assignee_profile = service.assignee.userprofile
                amount = service.time_required

                if service.service_type == 'request': # Creator requested help, so they pay
                    if creator_profile.time_credit < amount:
                        messages.error(request, "You do not have enough credits to complete this service.")
                        return redirect('dashboard')
                    creator_profile.time_credit -= amount
                    assignee_profile.time_credit += amount
                else: # Creator offered help, so they get paid
                    if assignee_profile.time_credit < amount:
                        messages.error(request, f"{service.assignee.username} does not have enough credits.")
                        return redirect('dashboard')
                    assignee_profile.time_credit -= amount
                    creator_profile.time_credit += amount

                creator_profile.save()
                assignee_profile.save()

                service.status = 'completed'
                service.save()
                messages.success(request, "Service completed and credits transferred successfully!")

        except UserProfile.DoesNotExist:
            messages.error(request, "A user profile was not found. Cannot complete transaction.")

    return redirect('dashboard')
