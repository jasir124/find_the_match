from django import forms
from .models import StudentSkill, Skill

class StudentSkillForm(forms.ModelForm):
    class Meta:
        model = StudentSkill
        fields = ['skill', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'skill': forms.Select(attrs={'class': 'form-select'})
        }
