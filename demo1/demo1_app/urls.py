from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('user_login',views.user_login,name='user_login'),
    path('user_register',views.user_register,name='user_register'),
    path('home',views.home,name='home'),
    path('upload/', views.upload_resource, name='upload'),
    path('search/', views.search_resources, name='search'),
    path('download/<int:resource_id>/', views.download_resource, name='download'),
]