from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Skill, Service, Review

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

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Rating (1-5)"
    )
    class Meta:
        model = Review
        fields = ['rating', 'comment']
