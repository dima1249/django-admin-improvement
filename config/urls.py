"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from timesheet import views
from timesheet.views import timesheet_list, submit_timesheet, TimesheetCreateView
from timesheet.views import timesheet_list_create

urlpatterns = [
    # Админ хэсэг
    path('admin/', admin.site.urls),

    # Timesheet-ийн гол хуудас, жагсаалт
    path('timesheets/', timesheet_list, name='timesheet_list'),

    # Нүүр хуудас (ганцхан жишээ - timesheet_list руу чиглүүлнэ)
    path('', timesheet_list, name='home'),

    # Timesheet шинэчлэх/нэмэх API (AJAX-тай холбоотой POST)
    path('submit/', submit_timesheet, name='submit_timesheet'),

    # Timesheet байгаа эсэхийг шалгах API (AJAX-тай)
    path('timesheet_exists/', views.timesheet_exists, name='timesheet_exists'),

    # Тухайн өдрийн timesheet-ийг авах API (AJAX-тай)
    path('get_timesheet/', views.get_timesheet, name='get_timesheet'),

    path('api/timesheet/create/', TimesheetCreateView.as_view(), name='timesheet-create'),

    path('api/timesheet/', timesheet_list_create, name='api_timesheet'),

    # AJAX endpoints
    path('ajax_timesheet/', views.ajax_timesheet, name='ajax_timesheet'),
    path('ajax/timesheet/check/', views.timesheet_exists, name='timesheet_exists'),
    path('ajax/timesheet/get/', views.get_timesheet, name='get_timesheet'),
]
