from django.shortcuts import render, redirect
from .forms import RegisterationForm, CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from dashboard.models import OrganizerDetails, EventStallUsers, Stalls
from django.contrib.auth.views import LoginView, LogoutView
from users.models import MyUser
from django.urls import reverse
from django.http import HttpResponseRedirect
import string
import random
from django.contrib.auth import logout as auth_logout
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import pdb
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def automatically_login(request, form):
    new_user = authenticate(username=form.cleaned_data['mobile'],
                            password="123",
                            )
    login(request, new_user)


def register(request, company_name, stall_text):
    organization = OrganizerDetails.objects.get(name=company_name)
    image = organization.login_background_image
    logo = organization.logo
    additional_login_field = organization.additional_login_field

    if request.user.id is not None:
        stall_id = Stalls.objects.get(unique_url=stall_text, organization=organization.id)
        try:
            # pdb.set_trace()
            EventStallUsers.objects.get(event_user_id=request.user.id, event_stall_id=stall_id)
            # check if user is stall user or normal user
            print(f"staff {MyUser.objects.get(id=request.user.id).is_staff}")
            if MyUser.objects.get(id=request.user.id).is_staff:
                return HttpResponseRedirect(reverse('main_website:stall_owner_chat',kwargs={'company_name': company_name, 'stall_text': stall_text}))
            return HttpResponseRedirect(
                reverse('main_website:main_page', kwargs={'company_name': company_name, 'stall_text': stall_text}))
        except:
            logout(request)
            return HttpResponseRedirect(
                reverse('users:register', kwargs={'company_name': organization.name, 'stall_text': stall_text}))

    if request.method == 'POST':
        registration_form = RegisterationForm(request.POST)  # ,additional_login_field = additional_login_field)
        stall_id = Stalls.objects.get(unique_url=stall_text, organization=organization.id)

        context = {}
        if registration_form.is_valid():
            print('weffds')
            registration_form.cleaned_data['mobile'] = registration_form.cleaned_data['mobile_number_form']
            print(registration_form.cleaned_data['mobile'])
            use_exist = False
            try:
                # check if user already exist
                MyUser.objects.get(mobile=registration_form.cleaned_data['mobile'])
                user_exist = True
            except:
                user_exist = False
            # return render(request,'registration/signup.html',context)

            if user_exist:
                user = MyUser.objects.get(mobile=registration_form.cleaned_data['mobile'])
                stall_user_exist = False
                stall_user = None

                try:
                    # check if user already present in stall.
                    print('stall donot exist')
                    EventStallUsers.objects.get(event_user_id=user.id, event_stall_id=stall_id)
                    stall_user_exist = True
                except:
                    stall_user_exist = False

                if not stall_user_exist:
                    stall_user = EventStallUsers.objects.create(event_user_id=user.id, event_stall_id=stall_id,
                                                                organizer_name=organization)
                    stall_user.save()
            else:
                print('wow3')
                new_user = registration_form.save(commit=False)
                new_user.mobile = new_user.mobile_number_form
                new_user.set_password('123')
                new_user.save()

                stall_user = EventStallUsers.objects.create(event_user_id=new_user.id, event_stall_id=stall_id,
                                                            organizer_name=organization)
                stall_user.save()

            # messages.success(request, "Account Successfully Created"
            # send_welcome_mail(registration_form.cleaned_data['email'],registration_form.cleaned_data['name'])
            context = {
                'registration_form': registration_form,
                'login_image': image,
                'company_name': company_name,
                'stall_text': stall_text,
                'logo': logo,
                'heading': organization.login_page_heading,
                'subheading': organization.login_page_subheading,
                'rotating_image': organization.brand_logo,
                'additional_login_field': additional_login_field,
            }
            # return render(request, "registration/thankyou.html")
            automatically_login(request, registration_form)

            if MyUser.objects.get(id=request.user.id).is_staff:
                return HttpResponseRedirect(reverse('main_website:stall_portal', kwargs={'company_name': company_name,'stall_text': stall_text}))

            return HttpResponseRedirect(
                reverse('main_website:main_page', kwargs={'company_name': company_name, 'stall_text': stall_text}))

        else:
            print('else')
            print(registration_form)
            print(registration_form.errors)
            context = {
            'registration_form': registration_form,
            'login_image': image,
            'company_name': company_name,
            'stall_text': stall_text,
            'logo': logo,
            'heading': organization.login_page_heading,
            'subheading': organization.login_page_subheading,
            'rotating_image': organization.brand_logo,
            'additional_login_field': additional_login_field,
            }
        return render(request, 'registration/signup_new.html', context)
    else:
        registration_form = RegisterationForm()  # additional_login_field = additional_login_field)
        registration_form.fields["mobile"].initial = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=25))
        context = {
            'registration_form': registration_form,
            'login_image': image,
            'company_name': company_name,
            'stall_text': stall_text,
            'logo': logo,
            'heading': organization.login_page_heading,
            'subheading': organization.login_page_subheading,
            'rotating_image': organization.brand_logo,
            'additional_login_field': additional_login_field,
        }
    return render(request, 'registration/signup_new.html', context)


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = self.kwargs["company_name"]  # kwargs['company_name']
        context['stall_text'] = self.kwargs["stall_text"]

        organization = None
        try:
            organization = OrganizerDetails.objects.get(name=self.kwargs["company_name"])
        except:
            raise Http404("Page doesnot Exist")
        image = organization.login_background_image
        logo = organization.logo
        context['login_image'] = image
        context['logo'] = logo
        context['heading'] = organization.login_page_heading
        context['subheading'] = organization.login_page_subheading
        context['rotating_image'] = organization.brand_logo
        return context

    def get_success_url(self):
        print('wow')
        company_name = self.kwargs['company_name']
        stall_text = self.kwargs['stall_text']
        return '{}'.format(
            reverse('main_website:main_page', kwargs={'company_name': company_name, 'stall_text': stall_text}))


class CustomLogoutView(LogoutView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = self.kwargs["company_name"]  # kwargs['company_name']
        context['stall_text'] = self.kwargs["stall_text"]

        organization = OrganizerDetails.objects.get(name=self.kwargs["company_name"])
        image = organization.login_background_image
        logo = organization.logo
        context['login_image'] = image
        context['logo'] = logo

        return context

    def dispatch(self, request, *args, **kwargs):
        # super().dispatch(request, *args, **kwargs)
        auth_logout(request)
        company_name = self.kwargs['company_name']
        stall_text = self.kwargs['stall_text']
        # next_page = self.get_next_page()
        # if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(
            reverse('users:login', kwargs={'company_name': company_name, 'stall_text': stall_text}))
    # return super().dispatch(request, *args, **kwargs)


def basic_login_redirect(request):
    organization = OrganizerDetails.objects.get(name='Synnex')
    stall_text = Stalls.objects.filter(organization=organization)[0].unique_url
    return HttpResponseRedirect(
        reverse('users:register', kwargs={'company_name': organization.name, 'stall_text': stall_text}))


def send_welcome_mail(user_email, user_name):
    MESSAGE = MIMEMultipart('alternative')
    subject = "Indian Food Nutrition Summit"
    MESSAGE['subject'] = subject
    MESSAGE['To'] = user_email
    MESSAGE['FROM'] = "webinarwall2020@gmail.com"
    body = """
            Dear {}, <br>
            <h4>Greetings of the Day !!</h4>
            <b>Thank you for registering with Synnex Group for the exclusive live 3D “INDIA FOOD NUTRITION SUMMIT  2020” We are glad to welcome you on board.</b><br><br>
            <u>Experience 3D Virtual Summit that we have organized in association with AIFPA, AFST(I), PAI & Indian Dietetic Association,  Below are the details for your reference : </u><br>
            Login link
            http://indiafoodnutritionsummit.webinarwall.com/login/Synnex/YSGOCM6BH2YOL6PCJ0NUR76ZX/

            <b><p style="background-color:yellow;">Attention : Please use your registered email id/Mobile Number to Login on the day of the Event ( No separate password required to Log In )</p> </b>

            <b>INDIA FOOD NUTRITION SUMMIT 2020</b><br>
            DATE : 25th Sept 2020       <br>
            Time : 09:30 am - 02:30 pm IST <br><br>

            KEY PANEL DISCUSSION SESSIONS -<br>

            •   Prebiotics and Probiotics: Creating a Healthier You<br>
            •   Food Fortification & Health: Enriching Foods, Enriching Lives<br> 
            •   Nutraceuticals : "Let food be thy medicine and medicine be thy food.<br> 
            •   COVID19 : The State and Future of the Nutrition Industry:<br>

            <b><p style="background-color:yellow;">We not only want you to participate, network and learn at the summit, but also want to ensure you’re rewarded for it! We are happy to announce an amazing contest – ‘The  Leadership Contest’. </p></b>

            <u>Refer below for  the Contest details:- </u><br>
            <b>
            1.  Synnex Group Linked in post will be live throughout, The participant has to post, like, Comment & Share on the posts. Interact More & Gain Points.<br>
            2.  Maximum Number of Exhibit Stall Visits<br>
            3.  Attending all Live sessions<br>
            4.  Maximum Number of Chatting and Meeting with the Sponsors at the exclusive live meeting rooms<br><br>
            </b>

            In this contest  - <b> <p style="background-color:yellow;">The participant with the highest point Score will get an Exciting brand New Smart Phone from Synnex Group</p></b>
            So login into the platform at <b>09: 30 am</b> sharp on <b>25th Sept 2020</b> and start collecting your points.
            <br>
            Stay tuned & updated by following our LinkedIn Page :<br><br> 
            https://www.linkedin.com/company/synnex-group <br>
            <br><br>
            <i>Your presence is awaited. Please feel free to reach out in case of any queries.</i>
            <br><br>
            <u>Contact us</u><br>
            Tel: +91 22 4612 7000<br>
            Fax:<br>
            Email: info@synnexgroup.com<br>

    """.format(user_name)
    HTML_BODY = MIMEText(body, 'html')
    MESSAGE.attach(HTML_BODY)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('webinarwall2020@gmail.com', 'Webinar@2020')
    server.sendmail(
        'webinarwall2020@gmail.com',
        user_email,
        MESSAGE.as_string()
    )
    server.quit()
