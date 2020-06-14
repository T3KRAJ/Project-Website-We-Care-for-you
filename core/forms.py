from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from core.models import Profile

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=200)

    class Meta:
        model = Profile
        fields = ['image', 'bio', ]

class DeactivateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(DeactivateUserForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = "Check this box if you are sure you want to delete this account."

    def clean_is_active(self):  
        # Reverses true/false for your form prior to validation
        #
        # You can also raise a ValidationError here if you receive 
        # a value you don't want, to prevent the form's is_valid 
        # method from return true if, say, the user hasn't chosen 
        # to deactivate their account
        is_active = not(self.cleaned_data["is_active"])
        return is_active