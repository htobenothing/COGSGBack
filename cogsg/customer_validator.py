import datetime
from rest_framework import serializers
from rest_framework.serializers import BaseSerializer
from .models import Member
from django.utils import timezone
def UniqueForWeekValidator(latestobj,date_field,new_date):
    
    old_date = getattr(latestobj,date_field)

    new_date = new_date.replace(tzinfo=timezone.get_default_timezone())
    start_week = old_date - datetime.timedelta(old_date.weekday())
    end_week = start_week + datetime.timedelta(7)

    print("start week {0}, end week {1}, new date{2}".format(start_week,end_week,new_date))
    if (new_date >= start_week) and (new_date <= end_week):
        message = 'The record already submit this week'
        raise serializers.ValidationError('Duplicate submit')
