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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grouped_choices = []
        for cat_code, cat_name in Skill.CATEGORY_CHOICES:
            skills_qs = Skill.objects.filter(category=cat_code).order_by('name')
            if skills_qs.exists():
                grouped_choices.append(
                    (cat_name, [(s.id, s.name) for s in skills_qs])
                )
        self.fields['skill'].choices = [('', '---------')] + grouped_choices
