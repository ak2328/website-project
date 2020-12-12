from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.layout import Layout, Submit, Row, Column
from .custom_layout_object import *

class StallsForm(forms.ModelForm):

    class Meta:
        model = Stalls
        exclude = ()

OrganizerDetailsFormSet = inlineformset_factory(
    OrganizerDetails, Stalls, form=StallsForm,
    fields=['stall_video_url','stall_web_link','stall_image_link','stall_front_image'], can_delete=False,min_num=11,max_num=11
    )


class OrganizerDetailsForm(forms.ModelForm):

    class Meta:
        model = OrganizerDetails
        fields = '__all__'
        # exclude = ['created_by', ]

    def __init__(self, *args, **kwargs):
        super(OrganizerDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                HTML('<h1>Expo meta</h1>'),
                Row('name',css_class = 'col-md-12'),
                Row('logo',css_class = 'col-md-12'),
                HTML('</br>'),
####################################################################
                HTML('<h1>Registeration_By</h1>'),
                HTML('<hr>'),                
                Row('additional_login_field',css_class='col-md-12'),
                HTML('</br>'),
                Row('brand_logo',css_class='col-md-12'),
#####################################################################
                HTML('<h1>Landing Page</h1>'),
                HTML('<hr>'),          
                Row(
                    Column('main_page_background_type',css_class = 'col-md-6'),
                    Column('main_page_background_url',css_class = 'col-md-6'),
                ),
########################################################################
                HTML('<h1>Lobby</h1>'),
                HTML('<hr>'),          
                Field('lobby_video_link',css_class = 'col-md-12'),
                Row(
                    Column('lobby_background_type',css_class = 'col-md-6'),               
                    Column('lobby_background_url',css_class = 'col-md-6'),                                   
                ), 
                Row(
                    Column('lobby_left_logo',css_class = 'col-md-6'),
                    Column('lobby_right_logo',css_class = 'col-md-6'),
                ),
                Field('lobby_banner_link',css_class='col-md-12'),
                HTML('<hr>'),  
                Row(
                    Column('hall_title_1',css_class = 'col-md-6'),
                    Column('hall_title_2',css_class = 'col-md-6'),
                ),
                Row(
                    Column('hall_title_3',css_class = 'col-md-6'),
                    Column('hall_title_4',css_class = 'col-md-6'),
                ),
                HTML('<hr>'),  
                Row(
                    Column('resource_1_name',css_class = 'col-md-6'),
                    Column('resource_1_link',css_class = 'col-md-6'),
                ),
                Row(
                    Column('resource_2_name',css_class = 'col-md-6'),
                    Column('resource_2_link',css_class = 'col-md-6'),
                ),
                Row(
                    Column('resource_3_name',css_class = 'col-md-6'),
                    Column('resource_3_link',css_class = 'col-md-6'),
                ),
                Row(
                    Column('resource_4_name',css_class = 'col-md-6'),
                    Column('resource_4_link',css_class = 'col-md-6'),
                ),
                HTML('</br>'),
#########################################################################
                HTML('<h1>Stall</h1>'),
                HTML('<hr>'),                
                Formset('titles'),                                
                HTML('</br>'),
#########################################################################                
                HTML('<h1>Auditorium</h1>'),
                HTML('<hr>'),                
                Field('auditorium_youtube_name'),
                Field('auditorium_keynote_track'),
                Field('auditorium_background_image'),
                HTML('</br>'),
#########################################################################
                HTML('<h1>Info Desk</h1>'),
                HTML('<hr>'),                
                Field('info_desk'),        
                Field('website_url'),        
                Field('info_background_image'),                
                HTML('</br>'),
#######################################################################
#                Field('website_url'),
                HTML('<h1>Exhibit Hall</h1>'),
                HTML('<hr>'),    
                Row(
                    Column('hall_logo_left',css_class = 'col-md-4'),
                    Column('hall_logo_center',css_class = 'col-md-4'),
                    Column('hall_logo_right',css_class = 'col-md-4'),
                ),           
                Field('hall_background_image'),                 
                HTML('</br>'),
#######################################################################
                HTML('<h1>Resource Center</h1>'),                
                Field('resource_ui_name'),
                HTML('<hr>'),                
                HTML('</br>'),
#######################################################################
                HTML('<h1>Social Lounge</h1>'),
                HTML('<hr>'),                                
                Field('social_lounge_name'), 
                Field('social_lounge_background_image'),                                                
                HTML('</br>'),
#######################################################################                
                HTML('<h1>Summit Lifetime</h1>'),
                HTML('<hr>'),                
                Field('validity_time'),
                HTML('</br>'),
########################################################################                
                HTML('<h1>Zoom</h1>'),
                HTML('<hr>'),                
#                Field('zoom_account_name'),
#                Field('zoom_password'),                
                HTML('</br>'),
#######################################################################
                HTML('<h1>Login</h1>'),
                HTML('<hr>'),                
                Field('login_background_image'),        
                HTML('</br>'),
                ButtonHolder(Submit('submit', 'save')),
                )
            )

