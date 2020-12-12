from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
	path('',views.basic_login_redirect,name='basic_login'),
    path('register/<str:company_name>/<str:stall_text>/',views.register,name = 'register'),
    path('login/<str:company_name>/<str:stall_text>/', views.CustomLoginView.as_view(), name='login'),
    path('logout/<str:company_name>/<str:stall_text>/', views.CustomLogoutView.as_view(), name='logout'),
]