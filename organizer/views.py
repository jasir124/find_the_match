from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from skills.models import StudentSkill, Skill
from accounts.models import CustomUser

@login_required
def search_view(request):
    user = request.user
    if user.role != 'ORGANIZER' and user.role != 'ADMIN':
        messages.error(request, 'Only organizers can access this page.')
        return redirect('home')

    skills = Skill.objects.all().order_by('category', 'name')
    return render(request, 'organizer/search.html', {'skills': skills})

@login_required
def results_view(request):
    user = request.user
    if user.role != 'ORGANIZER' and user.role != 'ADMIN':
        messages.error(request, 'Only organizers can access this page.')
        return redirect('home')

    skill_id = request.GET.get('skill_id')
    department = request.GET.get('department', '').strip()
    year = request.GET.get('year', '').strip()

    if not skill_id:
        messages.error(request, 'Please select a skill to search.')
        return redirect('search')

    try:
        skill = Skill.objects.get(id=skill_id)
    except Skill.DoesNotExist:
        messages.error(request, 'Invalid skill selected.')
        return redirect('search')

    # Filter StudentSkill based on the chosen skill
    results = StudentSkill.objects.filter(skill=skill, user__status='ACTIVE')

    # Optional filters
    if department:
        results = results.filter(user__department__icontains=department)
    if year:
        results = results.filter(user__year__icontains=year)

    # Sort by rating descending
    results = results.order_by('-rating')

    return render(request, 'organizer/results.html', {
        'results': results,
        'skill': skill,
        'department': department,
        'year': year
    })
