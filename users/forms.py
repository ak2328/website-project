from django import forms
from .models import MyUser
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import authenticate
from dashboard.models import OrganizerDetails

class RegisterationForm(forms.ModelForm):

	class Meta:
		model = MyUser
		fields = ('name','mobile','mobile_number_form','email','designation','type_of_available_services','when_do_you_plan_to_implement','email_id')
		labels = {
		    "mobile_number_form": "Mobile Number"
		}

	def __init__(self, *args, **kwargs):
		super(RegisterationForm, self).__init__(*args, **kwargs)
		# self.fields['email'].label = additional_login_field



class CustomAuthenticationForm(AuthenticationForm):
	error_messages = {
	    'invalid_login': _(
	        "Please enter correct Mobile Number"
	    ),
	    'inactive': _("This account is inactive."),
	}


	def clean(self):
	    username = self.cleaned_data.get('username')
	    password = 123
	    if username is not None and password:	    	
	        self.user_cache = authenticate(self.request, username=username, password=password)
	        if self.user_cache is None:
	            raise self.get_invalid_login_error()
	        else:
	            self.confirm_login_allowed(self.user_cache)

	    return self.cleaned_data    
