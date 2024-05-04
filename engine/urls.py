from django.urls import path
from . import views

urlpatterns = [
  # home page redirections
  path('home/', views.index, name='home'),
  path('', views.index, name='index'),
  path('list-entries/', views.list_entries, name='list-entries'),
  path('log_entry_click/', views.log_entry_click, name='log_entry_click'),
]