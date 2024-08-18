from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control'}))

	class Meta:
		model = User
		fields = ['username', 'email']

	def clean_username(self):
		username = self.cleaned_data['username']

		if ' ' in username:
			raise ValidationError("Username cannot contain spaces.")

		if len(username) < 3 or len(username) > 12:
			raise ValidationError("Username must be between 3 and 12 characters.")
			
		return username
