from django.urls import path
from . import views

urlpatterns = [
  # home page redirections
  path('home/', views.index, name='home'),
  path('', views.index, name='index'),
  # general redirections
  path('list-entries/', views.list_entries, name='list-entries'),
  path('display-entry/', views.display_entry, name='display-entry'),
  # path('list-all-entries/<int:first_id>-<int:last_id>-<int:prev>/', views.list_all_entries, name='list-entries-parameters'),
]