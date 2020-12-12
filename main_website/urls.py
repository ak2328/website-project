from django.urls import path
from . import views


app_name = 'main_website'

urlpatterns = [
    path('homepage/<str:company_name>/<str:stall_text>/', views.home_page, name='main_page'),
    path('lobby/<str:company_name>/<str:stall_text>/', views.lobby_page, name='lobby'),    
    path('auditorium/<str:company_name>/<str:stall_text>/', views.auditorium, name='auditorium'),     
    path('info_desk/<str:company_name>/<str:stall_text>/', views.info_desk, name='info_desk'),    
    path('exhibit_hall/<str:company_name>/<str:stall_text>/', views.exhibit_hall, name='exhibit_hall'),    
    path('resource_center/<str:company_name>/<str:stall_text>/', views.resource_center, name='resource_center'),    
    path('social_lounge/<str:company_name>/<str:stall_text>/', views.social_lounge, name='social_lounge'),                       
    path('zoom_start/', views.zoom_start, name='zoom_start'),    
    path('stall/<str:company_name>/<str:stall_text>/',views.stall,name='stalls'),                       
    path('stall_iframe',views.stall_iframe,name='stall_iframe'),
    path('stall_portal/<str:company_name>/<str:stall_text>/',views.stall_portal,name='stall_portal'),
    path('stall_details/<str:company_name>/<str:stall_text>/',views.stall_details,name='stall_details'),
    path('auditorium_owner/<str:company_name>/',views.auditorium_owner,name='auditorium_owner'),        
    path('stall_owner_page/<str:company_name>/',views.stall_owner_page,name='stall_owner_page'),
    path('stall_owner_chat/<str:company_name>/<str:stall_text>/',views.stall_owner_chat,name='stall_owner_chat'),    
    path('question',views.question,name = 'question'),
    path('photobooth/',views.photobooth,name='photobooth'),
    path('stall_analytics/<str:company_name>/<str:stall_text>/',views.stall_analytics,name='stall_analytics'),
    path('stall_add_documents/<str:company_name>/<str:stall_text>/',views.stall_add_documents,name='stall_add_documents'),
    path('stall_add_sales_representative/<str:company_name>/<str:stall_text>/',views.stall_add_sales_representatives,name='stall_add_sales_representatives'),


    path('first_floor/<str:company_name>/<str:stall_text>/',views.first_floor,name="first_floor"),
    path('first_floor/room1/<str:company_name>/<str:stall_text>/',views.first_floor_link1,name="first_floor_link1"),
    path('first_floor/room2/<str:company_name>/<str:stall_text>/',views.first_floor_link2,name="first_floor_link2"),
    path('first_floor/room3/<str:company_name>/<str:stall_text>/',views.first_floor_link3,name="first_floor_link3"),


    path('submit_polling_results/<str:company_name>/<str:stall_text>/',views.submit_polling_results,name="submit_polling_results"),
    path('update_doc/<str:company_name>/<str:stall_text>/',views.update_document,name="update_document"),
    path('update_social_media_link/<str:company_name>/<str:stall_text>/',views.update_social_media_link,name="update_social_media_link"),
    path('new_doc/<str:company_name>/<str:stall_text>/',views.new_document,name="new_document"),
    path('new_representative/<str:company_name>/<str:stall_text>/',views.new_representative,name="new_representative"),
    path('update_representative/<str:company_name>/<str:stall_text>/',views.update_representative,name="update_representative"),
    path('schedule_call/<str:company_name>/<str:stall_text>/',views.schedule_call_by_user,name="schedule_call"),

    path('feedback',views.FeeBack.as_view(),name='feedback')
]