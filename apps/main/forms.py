from django import forms
from django.utils.translation import gettext_lazy as _

CHOICES = [('1', _('Client')), ('2', _('Partner')),]

class UserForm(forms.Form):
	user_type = forms.ChoiceField(label=_('I am:'), initial='1', widget=forms.RadioSelect, choices=CHOICES)
	name = forms.CharField(label=_('Name'), max_length=100)
	email = forms.EmailField(required=True)
	password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
	password2 = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput)
	phone = forms.CharField(label=_('Phone'), max_length=13)
	address = forms.CharField(label=_('Address'), max_length=200)
	nif = forms.CharField(max_length=9)
	
	def clean_password2(self):
		if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
			raise forms.ValidationError(_('Invalid password confirmation'))
