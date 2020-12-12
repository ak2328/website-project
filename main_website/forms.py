from django import forms
from users.models import MyUser
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import authenticate
from dashboard.models import OrganizerDetails
from main_website.models import FeedBack
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from crispy_forms.layout import Layout, Submit, Row, Column


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = FeedBack
        fields = '__all__'
        labels = {
            "question1": "Please rate your overall satisfaction with the virtual conference",
            "question2": "Please rate your overall satisfaction with the exhibits area",
            "question3": "Please rate your overall satisfaction with the format of the conference",
            "question4": "Please rate your overall satisfaction with the access and convenience with the Platform use",
            "question5": "Please rate your overall satisfaction with the access and convenience with the Platform used ",
            "question6": "Please rate Quality of Audio & Visuals ",
            "question7": "The Quality of our sponsors / partners for the summit",
            "question8": "Have your organization embarking on any strategic initiatives approved to improve on Technology / IOT etc.?",
            "question9": "The likely time period of undertaking these strategic initiatives is",
            "question10": "Please provide any comments you have on future conference  platforms,  topics, speakers or general suggestions regarding the conference",
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Row('question1'),
                Row('question2'),
                'question3',
                'question4',
                'question5',
                'question6',
                'question7',
                'question8',
                'question9',
                'question10',
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )