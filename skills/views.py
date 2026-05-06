from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentSkill, Skill
from .forms import StudentSkillForm
from accounts.models import CustomUser

@login_required
def profile_view(request):
    user = request.user
    if user.role != 'STUDENT':
        messages.error(request, 'Only students have profiles.')
        return redirect('home')
        
    skills = StudentSkill.objects.filter(user=user)
    return render(request, 'skills/profile.html', {'user': user, 'skills': skills})

@login_required
def edit_profile_view(request):
    user = request.user
    if user.role != 'STUDENT':
        messages.error(request, 'Only students can edit skills.')
        return redirect('profile')

    skills = StudentSkill.objects.filter(user=user)
    
    if request.method == 'POST':
        if 'add_skill' in request.POST:
            form = StudentSkillForm(request.POST)
            if form.is_valid():
                student_skill = form.save(commit=False)
                student_skill.user = user
                # Check for duplicate
                if StudentSkill.objects.filter(user=user, skill=student_skill.skill).exists():
                    messages.error(request, 'You have already added this skill. Update it instead.')
                else:
                    student_skill.save()
                    messages.success(request, 'Skill added successfully.')
                return redirect('edit_profile')
        elif 'delete_skill' in request.POST:
            skill_id = request.POST.get('skill_id')
            skill_to_delete = get_object_or_404(StudentSkill, id=skill_id, user=user)
            skill_to_delete.delete()
            messages.success(request, 'Skill removed.')
            return redirect('edit_profile')
        elif 'update_skill' in request.POST:
            skill_id = request.POST.get('skill_id')
            new_rating = request.POST.get('rating')
            skill_to_update = get_object_or_404(StudentSkill, id=skill_id, user=user)
            try:
                rating = int(new_rating)
                if 1 <= rating <= 10:
                    skill_to_update.rating = rating
                    skill_to_update.save()
                    messages.success(request, 'Skill rating updated.')
                else:
                    messages.error(request, 'Rating must be between 1 and 10.')
            except ValueError:
                messages.error(request, 'Invalid rating.')
            return redirect('edit_profile')

    add_form = StudentSkillForm()
    return render(request, 'skills/edit_profile.html', {
        'skills': skills,
        'add_form': add_form
    })
