from rest_framework import serializers
from cogsg.models import Member, Attend, District
from django.contrib.auth.models import User, Group
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from .customer_validator import UniqueForWeekValidator


class MemberSerializer(serializers.ModelSerializer):
    # ModelSerializer is the shortcut of making fields serializer by ourself
    # logic about the serializer/deserializer:
    # 1. serialize the model instance, then JsonRender to translate into python native datatype:json.
    # 2. convert json to instance, use BytesIO,JsonParser and serialzer to convert to a object instance
    Attend = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Attend.objects.all()
    )

    class Meta:
        model = Member
        fields = ('Member_ID', 'Name', 'Member_Type',
                  'District_ID', 'Email', 'Phone', 'Status',
                  'Attend', "Create_Date")


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = ['District_ID', 'Zone', 'District_Name', 'Address', 'PostCode', 'Status']


class AttendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attend
        fields = ['Attend_ID', 'Member_ID', 'Create_Date',
                  'Lords_Table', 'Prayer_Meeting', 'Morning_Revival',
                  'Bible_Reading', 'Small_Group']

        # validators = [
        #     UniqueForWeekValidator(
        #         latestobj=Attend.objects.all(),
        #         date_field="Create_Date",
        #
        #         new_date=datetime.now()
        #     )
        # ]
    def create(self, validated_data):
        """
        check whether the record already submit or not in current week
        :param validated_data:
        :return:
        """
        date = datetime.today()
        member_id = validated_data["Member_ID"]
        queryset = Attend.objects.all().filter(Member_ID=member_id).order_by("-Attend_ID")

        if len(queryset) > 0:
            latestAttend = queryset[0]
            UniqueForWeekValidator(latestobj=latestAttend, date_field="Create_Date", new_date=date)

            instance = Attend.objects.create(**validated_data)
            return instance

        return Attend.objects.create(**validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
