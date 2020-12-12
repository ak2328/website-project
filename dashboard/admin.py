from django.contrib import admin
from .models import Stalls, OrganizerDetails
import urllib.parse
import pandas as pd
import time
from main_website.models import Analytics
from .models import Stall_Owner_documents
from django.http import HttpResponse
# Register your models here.
class StallsAdminInline(admin.TabularInline):

	model = Stalls
	# verbose_name = 'Kiosk Sales'
	# verbose_name_plural = 'Kiosk Sales List'

	# show one empty instance when creating
	# no empty instance when editing
	def get_extra(self, request, obj=None, **kwargs):
		if obj :
			return 0
		else:
			return 1	  
	readonly_fields = ['unique_url']


@admin.register(OrganizerDetails)
class OrganizerDetailsAdmin(admin.ModelAdmin):
	search_fields =['name']
	list_display =['id','name', 'website_url']
	# list_editable = ['order_status']
	inlines = [StallsAdminInline]
	actions = ['download_pagewise_analytics','download_stall_analytics']

	def download_pagewise_analytics(self, request, queryset):
		# for entry in queryset:
		return self.generate_analytics_csv(urllib.parse.quote(queryset[0].name))

	def download_stall_analytics(self, request, queryset):
		return self.generate_stall_csv(urllib.parse.quote(queryset[0].name))


	def generate_analytics_csv(self,company_name):
		df = pd.DataFrame(Analytics.objects.filter(company_name = company_name).values())
		df['time']  = df['end_time'] - df['start_time']
		df['time'] = df['time'].apply(lambda x: x.seconds)
		df_pagewise = df.groupby('page_name').agg({
			'user_id_id':'count', 
			'time':'mean'
		})
		df_pagewise.reset_index(inplace = True)
		df_pagewise.columns = ['page','clicks','average time']
		return self.download_file(df_pagewise,'page_analytics.csv')

	def generate_stall_csv(self,company_name):
		df = pd.DataFrame(Analytics.objects.filter(company_name = company_name).values())
		df['time']  = df['end_time'] - df['start_time']
		df['time'] = df['time'].apply(lambda x: x.seconds)
		df_stallwise = df[df.page_name.str.contains('stall_')].groupby(['page_name','stall_name']).agg({
			'user_id_id':'count', 
			'time':'mean'
		})
		df_stallwise.reset_index(inplace = True)
		df_stallwise.columns = ['page','stall','click','time']
		return self.download_file(df_stallwise,'stall_analytics.csv')		

	def download_file(self,df,filename):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=' + filename

		df.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")
		return response

admin.site.register(Stall_Owner_documents)