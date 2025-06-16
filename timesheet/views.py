from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Timesheet
from django.utils.timezone import now, localtime  
from django.views.decorators.http import require_GET, require_http_methods
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import TimesheetSerializer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
import time

#  DRF API View: POST - /api/timesheet/create/
class TimesheetCreateView(generics.CreateAPIView):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer  

    def create(self, request, *args, **kwargs):
        time.sleep(1)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        timesheet = serializer.instance

        data = {
            'success': True,
            'message': 'Timesheet entry created successfully',
            'id': timesheet.id,
            'date': str(timesheet.date),
            'time': timesheet.time.strftime('%H:%M:%S'),
            'day': timesheet.date.strftime('%a')
        }
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

#  Аль алинд нь зориулагдсан: /api/timesheet/ GET/POST
@csrf_exempt
def timesheet_list_create(request):
    if request.method == 'GET':
        timesheets = Timesheet.objects.all().order_by('-date', '-time')
        data = [{
            'id': ts.id,
            'date': ts.date.strftime('%Y-%m-%d'),
            'time': ts.time.strftime('%H:%M'),
            'employee': ts.employee
        } for ts in timesheets]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            ts = Timesheet.objects.create(
                date=data['date'],
                time=data['time'],
                employee=data.get('employee', 'Anonymous')
            )
            return JsonResponse({
                'success': True,
                'id': ts.id,
                'date': str(ts.date),
                'time': str(ts.time),
                'employee': ts.employee,
                'day': ts.date.strftime('%a')
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


#  HTML-д зориулагдсан timesheet list view
def timesheet_list(request):
    times = ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    today = localtime(now())
    today_day = today.strftime('%a')

    timesheets = Timesheet.objects.all()
    timesheet_map = {day: {time: None for time in times} for day in days}

    for ts in timesheets:
        day = ts.date.strftime('%a')
        time = ts.time.strftime('%H:%M')
        if day in timesheet_map and time in timesheet_map[day]:
            timesheet_map[day][time] = ts

    context = {
        'times': times,
        'days': days,
        'today_day': today_day,
        'timesheet_map': timesheet_map,
    }
    return render(request, 'timesheet_list.html', context)


#  AJAX POST timesheet
@csrf_exempt
def ajax_timesheet(request):
    if request.method == 'POST':
        time.sleep(1)
        try:
            data = json.loads(request.body)
            date = data.get('date')
            time = data.get('time')
            employee = request.user.username if request.user.is_authenticated else "Anonymous"


            timesheet = Timesheet.objects.create(
                date=date,
                time=time,
                employee=employee
            )

            return JsonResponse({
                'success': True,
                'message': 'Timesheet entry created successfully',
                'id': timesheet.id,
                'date': str(timesheet.date),
                'time': str(timesheet.time),
                'day': timesheet.date.strftime('%a')
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


#  GET /timesheet_exists/
@require_GET
def timesheet_exists(request):
    date = request.GET.get('date')
    time = request.GET.get('time')
    ts = Timesheet.objects.filter(date=date, time=time).first()
    if ts:
        return JsonResponse({
            'exists': True,
            'id': ts.id,
            'date': str(ts.date),
            'time': str(ts.time),
        })
    else:
        return JsonResponse({'exists': False})


#  GET /get_timesheet/
@require_GET
def get_timesheet(request):
    date = request.GET.get('date')
    time = request.GET.get('time')
    ts = Timesheet.objects.filter(date=date, time=time).first()
    if ts:
        return JsonResponse({
            'exists': True,
            'id': ts.id,
            'date': str(ts.date),
            'time': str(ts.time),
        })
    else:
        return JsonResponse({'exists': False})


#  Submit from HTML form (POST)
@login_required
def submit_timesheet(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        employee = request.POST.get('employee')

        exists = Timesheet.objects.filter(date=date, time=time).exists()
        if exists:
            messages.error(request, 'Энэ цагийн зай аль хэдийн захиалагдсан байна!')
        else:
            Timesheet.objects.create(
                date=date, 
                time=time,
                employee=employee
            )
            messages.success(request, 'Цагийн бүртгэл амжилттай хадгалагдлаа!')
    return redirect('timesheet_list')


#  Админд зориулсан бүрэн timesheet data
@staff_member_required
@require_http_methods(["GET"])
def get_timesheet_data(request):
    try:
        timesheets = Timesheet.objects.all().order_by('-date', '-time')
        data = [{
            'date': ts.date.strftime('%Y-%m-%d'),
            'time': ts.time.strftime('%H:%M'),
            'employee': ts.employee
        } for ts in timesheets]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
