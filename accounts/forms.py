from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    college_id_image = forms.ImageField(required=True, label="Upload College ID")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'department', 'year', 'college_id_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
