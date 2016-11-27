from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.
from .data import MemberType, Zone
from datetime import datetime


class District(models.Model):
    District_ID = models.AutoField(primary_key=True)
    Zone = models.CharField(max_length=3, choices=Zone)
    District_Name = models.CharField(max_length=50)
    Create_Date = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    Address = models.CharField(max_length=120)
    PostCode = models.CharField(max_length=20)
    Status = models.BooleanField(default=True)

    def __str__(self):
        return "Zone {0}-{1}".format(self.Zone, self.District_Name)


class Member(models.Model):
    Member_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50,unique=True)
    Given_Name = models.CharField(max_length=50, blank=True)
    Family_Name = models.CharField(max_length=50, blank=True)
    Other_Name = models.CharField(max_length=120, blank=True)
    Member_Type = models.CharField(max_length=1, choices=MemberType)
    District_ID = models.ForeignKey(District, on_delete=models.CASCADE, default='0')
    Phone = models.CharField(max_length=50)
    Email = models.CharField(max_length=120, default='', blank=True)
    Create_Date = models.DateTimeField(auto_now_add=True)
    Status = models.BooleanField(default=True)

    def __str__(self):
        return "{0}:{1}".format(self.Member_ID, self.Name)


class Attend(models.Model):
    Attend_ID = models.AutoField(primary_key=True)
    Member_ID = models.ForeignKey(Member, related_name='Attend', on_delete=models.CASCADE)
    Create_Date = models.DateTimeField(auto_now_add=True)
    Lords_Table = models.BooleanField(default=False)
    Prayer_Meeting = models.BooleanField(default=False)
    Morning_Revival = models.BooleanField(default=False)
    Bible_Reading = models.BooleanField(default=False)
    Small_Group = models.BooleanField(default=False)

    def __str__(self):
        return "{0}".format(self.Attend_ID)

