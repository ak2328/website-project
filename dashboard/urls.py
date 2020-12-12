from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
	# path('', views.HomepageView.as_view(), name='homepage'),
	# path('dashboard/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('create/', views.DashboardCreate.as_view(), name='collection_dashboard'),
	]