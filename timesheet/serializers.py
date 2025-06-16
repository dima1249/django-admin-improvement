from rest_framework import serializers
from .models import Timesheet
#timesheetiin ugugdliig json helbert hurvulne
class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = '__all__' #modeliin bvh talbariig serializ hiine
