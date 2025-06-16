from django.urls import path
from . import views

urlpatterns = [
    path('', views.timesheet_list, name='timesheet_list'),
    path('api/timesheet/create/', views.TimesheetCreateView.as_view(), name='timesheet_create'),
    path('api/timesheet/', views.timesheet_list_create, name='timesheet_list_create'),
    path('api/timesheet/exists/', views.timesheet_exists, name='timesheet_exists'),
    path('api/timesheet/get/', views.get_timesheet, name='get_timesheet'),
] 