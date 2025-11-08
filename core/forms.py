from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Skill, Service

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class ProfileSkillUpdateForm(forms.Form):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Your Skills"
    )

class ServiceCreationForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'service_type', 'skill', 'time_required']
        widgets = {
            'service_type': forms.RadioSelect
        }
