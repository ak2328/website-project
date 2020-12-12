from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.db import transaction
from django.http import HttpResponse
import random
import string
from .models import Stalls
from users.models import MyUser


# Create your views here.
class DashboardCreate(CreateView):
    model = OrganizerDetails
    template_name = 'dashboard/dashboard.html'
    form_class = OrganizerDetailsForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(DashboardCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = OrganizerDetailsFormSet(self.request.POST, self.request.FILES)
        else:
            data['titles'] = OrganizerDetailsFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        temp_url = ''
        self.object = None
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
            else:
                print(titles.errors)
            unique_stall_urls = ''
            # titles.save()
            # for title in titles:
            #     title.stall_admin_link = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 25)) 
            #     title.unique_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 25)) 
            #     temp_url = title.unique_url
            #     unique_stall_urls = unique_stall_urls + '</br>' + '127.0.0.1:8000/login/' + title.unique_url
            # titles.save()

            stalls = Stalls.objects.filter(organization=self.object)
            for stall in stalls:
                stall.stall_admin_link = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
                stall.unique_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
                temp_url = stall.unique_url
                unique_stall_urls = unique_stall_urls + '</br>' + '127.0.0.1:8000/login/' + stall.unique_url
                stall.save()
                MyUser.objects.create_staff_user(stall.unique_url, '123123')

        unique_stall_urls = '<h4>' + unique_stall_urls + '</h4>'
        output_url = '<h1> Registeration Link </h1></br> 127.0.0.1:8000/login/' + str(
            self.object.name) + '/' + temp_url + '</br></br></br><h1> Stall Link </h1></br>'
        output_url = output_url + unique_stall_urls

        # return super(DashboardCreate, self).form_valid(form)
        return HttpResponse(output_url)

        # def get_success_url(self):
    #     return HTTPResponse('<h4>unique_stall_urls</h4>')   #reverse_lazy('mycollections:homepage')
