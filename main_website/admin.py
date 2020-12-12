
from django.contrib import admin

# Register your models here.

from .models import Notification,Message,Analytics,Question,ChannelOnlineCount,partners_tab,call_schedules,poll, Permanent_Poll_Answers, another_poll_answers

# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['id','reciever','author','count']

# admin.site.register(Notification, NotificationAdmin)


# class MessageAdmin(admin.ModelAdmin):
#     list_display = ['id','author','content','author_reciever_string']

# admin.site.register(Message, MessageAdmin)


class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['id','page_name','company_name','stall_name','start_time','end_time','user_id']
    
admin.site.register(Analytics, AnalyticsAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user','question']

admin.site.register(Question, QuestionAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['author','content','timestamp','reciever','seen_status','author_reciever_string']
    search_fields = ['reciever__mobile','author__mobile']

admin.site.register(Message, MessageAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['author_reciever_string','reciever','author','count']

admin.site.register(Notification, NotificationAdmin)



class ChannelOnlineCountAdmin(admin.ModelAdmin):
    list_display = ['author_reciever_string','count']

admin.site.register(ChannelOnlineCount, ChannelOnlineCountAdmin)

#add organizer partners
class partners_tabAdmin(admin.ModelAdmin):
	list_display = ['image','partner_name']
	exclude = ['stall_id']

admin.site.register( partners_tab,partners_tabAdmin)

admin.site.register(call_schedules)

admin.site.register(poll)

admin.site.register(Permanent_Poll_Answers)

