from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AddHoodForm(forms.ModelForm):
  class Meta:
    model = Neighbourhood
    fields = ['name','location','description','police_dept','health_dept']
    exclude = ['posted_on']


class AddBusinessForm(forms.ModelForm):
	class Meta:
		model = Business
		fields = ['name','email','description']

class UpdateProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['bio']

class AddPostForm(forms.ModelForm):
  class Meta:
    model = Posts
    fields = ['topic','post']

