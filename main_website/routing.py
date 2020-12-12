# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/notifications/$', consumers.NotificationSocketHome),    
    re_path(r'ws/groupchat/$', consumers.ChatGroupConsumer),
    re_path(r'ws/analytics/$', consumers.AnalyticsConsumer),  
    re_path(r'ws/auditorium/(?P<organization_name>\w+)', consumers.ChatAuditorium),
    re_path(r'ws/infocenter/(?P<organization_name>\w+)', consumers.ChatAuditorium),    
]



