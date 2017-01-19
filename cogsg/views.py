from django.shortcuts import render
from rest_framework import viewsets, status, request
from rest_framework.decorators import list_route, detail_route, api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMultiAlternatives
from .serializers import MemberSerializer, DistrictSerializer, AttendSerializer, UserSerializer
from .models import Member, District, Attend
from datetime import datetime, timedelta
import smtplib

# Create your views here.

class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()

    @list_route()
    def active(self, req):
        active_members = Member.objects.all().filter(Status=True).order_by('Name')
        serializer = self.get_serializer(active_members, many=True)
        return Response(serializer.data)


class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class AttendViewSet(viewsets.ModelViewSet):
    serializer_class = AttendSerializer
    queryset = Attend.objects.all()

    @list_route()
    def weekly(self, req):
        date = req.GET
        print("this is date:")

        start_week = date - timedelta(date.weekday())
        end_week = start_week + timedelta(7)
        weekly_data = Attend.objects.all().filter(Create_Date__range=[start_week, end_week])

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


@api_view(['POST'])
def sendStaticEmail(req):
    """

    :param req:
    :return:
    """
    if req.method == "POST":
        statistic = req.data

        currdate = datetime.today()
        currWeekDay = currdate.isoweekday()
        dateformt = "%m/%d/%y"
        print(statistic['Children'])
        start = (currdate - timedelta(days=currWeekDay + 6)).strftime(dateformt)
        lordDay = (currdate - timedelta(days=currWeekDay)).strftime(dateformt)

        subject = "Weekly Report for CommonWealth: {0} -- {1}".format(start, lordDay)
        fromEmail = "htobenoting@gmail.com"
        toEmail = ["htobenothing@gmail.com"]
        htmlContent = "<label>Dear ChurchOffice:</label> <p>Here is the statistic for CommonWealth :</p>" \
                      "<table class='table'> <tr> <td>Lord's day meeting</td> <td>{0}</td> " \
                      "</tr> <tr> <td>Morning Revival</td> <td>{1}</td> " \
                      "</tr> <tr> <td>Bible Reading</td> <td>{2}</td> </tr> " \
                      "<tr> <td>Small group/home meeting</td> <td>{3}</td> </tr> " \
                      "<tr> <td>Prayer Meeting</td> <td>{4}</td> </tr> " \
                      "<tr> <td>Children</td> <td>{5}</td> </tr> </table> "\
            .format(statistic["Lords_Table"],statistic["Morning_Revival"],statistic["Bible_Reading"],
                    statistic["Small_Group"],statistic["Prayer_Meeting"],statistic["Children"])
        msg = EmailMultiAlternatives(subject=subject,from_email=fromEmail,to=toEmail)
        msg.attach_alternative(htmlContent,"text/html")
        try :
            msg.send(fail_silently=False)
            return Response("Send SuccessFul", status=status.HTTP_200_OK)
        except Exception:
            return Response("Email fail",status=status.HTTP_400_BAD_REQUEST)
