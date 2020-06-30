from django import forms
from .models import Partner
from django.contrib.auth.models import User

IS_PARTNER_CHOICES = [
	('Yes', 'Yes'),
	('No', 'No')
]

class SignupForm(forms.Form):
 	username = forms.CharField(max_length=60, required = True)
 	password = forms.CharField(max_length=255, widget=forms.PasswordInput)
 	email = forms.EmailField(max_length=255)
 	first_name = forms.CharField(max_length=255, required = True)
 	last_name = forms.CharField(max_length=255, required = True)
 	is_partner = forms.ChoiceField(required=True, choices=IS_PARTNER_CHOICES)

class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, required = True)
	password = forms.CharField(max_length=255, widget=forms.PasswordInput)


class PartnerProfileForm(forms.ModelForm):

	class Meta:
		model = Partner
		exclude = ('created_on', 'modified_on')
