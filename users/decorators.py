from django.core.exceptions import PermissionDenied
from django.http import Http404
from dashboard.models import OrganizerDetails,EventStallUsers, Stalls
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
def organization_exist(function=None):
	def wrap(request, *args, **kwargs):
		try:
			entry = OrganizerDetails.objects.get(login_url=kwargs['company_name'])
			stall_text = Stalls.objects.get(unique_url=kwargs['stall_text'])			
			return function(request, *args, **kwargs)
		except:
			raise Http404("Page doesnot Exist")
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap


def user_authorized_for_page(function=None):
	def wrap(request, *args, **kwargs):
		try:
			entry = OrganizerDetails.objects.get(name=kwargs['company_name'])
			stall_text = Stalls.objects.get(unique_url=kwargs['stall_text'])	  
			try:
				EventStallUsers.objects.get(event_user_id = request.user.id,organizer_name = entry)
				return function(request, *args, **kwargs)
			except:
				messages.error(request, "Please Register for this event")           
				return HttpResponseRedirect(reverse('users:login', kwargs={'company_name':kwargs['company_name'],'stall_text':kwargs['stall_text']}))
		except:
			raise Http404("Page doesnot Exist")
	return wrap

    # def wrap(request, *args, **kwargs):
    #     if request.user.profile.userStatus == "admin":
    #         return view_func(request, *args, **kwargs)
    #     else:
    #         return render(request, "dashboard/404.html")
    # return wrap

