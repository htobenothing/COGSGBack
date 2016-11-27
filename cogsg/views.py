from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import MemberSerializer, DistrictSerializer, AttendSerializer, UserSerializer
from .models import Member, District, Attend


# Create your views here.

class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()

    @list_route()
    def active(self, req):
        active_members = Member.objects.all().filter(Status=True)
        serializer = self.get_serializer(active_members, many=True)
        return Response(serializer.data)


class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class AttendViewSet(viewsets.ModelViewSet):
    serializer_class = AttendSerializer
    queryset = Attend.objects.all()

    # def create(self, request, *args, **kwargs):
    #
    #     serializer = self.serializer_class(data=request.data)
    #
    #     if serializer.is_valid():
    #         print(serializer.is_valid())
    #         Attend.objects.create(**serializer.validated_data)
    #         return Response(serializer.instance, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
