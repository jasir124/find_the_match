from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import StudentRegistrationForm
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'STUDENT'
            user.status = 'PENDING'
            user.save()
            messages.success(request, 'Registration successful. Please wait for admin approval.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.status == 'ACTIVE' or user.is_superuser:
                    login(request, user)
                    messages.success(request, f"You are now logged in as {username}.")
                    if user.is_superuser or user.role == 'ADMIN':
                        return redirect('admin_dashboard')
                    elif user.role == 'ORGANIZER':
                        return redirect('search')
                    else:
                        return redirect('profile')
                else:
                    messages.error(request, 'Your account is pending admin approval or rejected.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('login')

def home_redirect_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'ORGANIZER':
            return redirect('search')
        else:
            return redirect('profile')
    return redirect('login')

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'ADMIN')

@user_passes_test(is_admin, login_url='login')
def admin_dashboard_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        target_user = CustomUser.objects.filter(id=user_id).first()
        
        if target_user:
            if action == 'approve':
                target_user.status = 'ACTIVE'
                target_user.save()
                messages.success(request, f'User {target_user.username} approved.')
            elif action == 'reject':
                target_user.status = 'REJECTED'
                target_user.save()
                messages.warning(request, f'User {target_user.username} rejected.')
        return redirect('admin_dashboard')

    from skills.models import StudentSkill
    
    # Get all users except superusers for the list
    pending_users = CustomUser.objects.filter(status='PENDING', is_superuser=False).order_by('-date_joined')
    active_users = CustomUser.objects.filter(status='ACTIVE', is_superuser=False).order_by('-date_joined')
    
    analytics = {
        'total_students': CustomUser.objects.filter(role='STUDENT', is_superuser=False).count(),
        'active_students': CustomUser.objects.filter(role='STUDENT', status='ACTIVE', is_superuser=False).count(),
        'pending_students': CustomUser.objects.filter(role='STUDENT', status='PENDING', is_superuser=False).count(),
        'total_organizers': CustomUser.objects.filter(role='ORGANIZER', is_superuser=False).count(),
        'total_skills_mapped': StudentSkill.objects.count(),
    }
    
    return render(request, 'accounts/admin_dashboard.html', {
        'pending_users': pending_users,
        'active_users': active_users,
        'analytics': analytics
    })
