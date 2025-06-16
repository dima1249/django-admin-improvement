from django.contrib import admin
from .models import Timesheet
from django.urls import reverse
from django.http import HttpResponseRedirect

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'employee')
    list_filter = ('date', 'employee')
    search_fields = ('employee',)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        date = request.GET.get('date')
        time = request.GET.get('time')
        if date:
            initial['date'] = date
        if time:
            initial['time'] = time
        return initial

    def response_add(self, request, obj, post_url_continue=None):
        url = reverse('admin:timesheet_timesheet_changelist')  
        return HttpResponseRedirect(url)
