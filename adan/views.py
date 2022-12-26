from .serializers import *
from rest_framework import viewsets,generics,permissions,status,authentication
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login
from rest_framework.views import APIView
from datetime import datetime
import json
# Create your views here.
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    @extend_schema(description='adan Login api ', methods=["post"],parameters=[LoginRequestBodySerializer],responses=LoginResponseSerializer  
    ,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
class LiveEventView(generics.CreateAPIView):
    """
    endpoint to create events to run immediately
    """
    authentication_classes=(TokenAuthentication,)
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = LiveAudioSerializers
    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            LiveAudioSerializers,
        ],
        # override default docstring extraction
        description='More descriptive text',
        # provide Authentication class that deviates from the views default
        auth=TokenAuthentication,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
        # attach request/response examples to the operation.
        examples=[
            OpenApiExample(
                'Example 1',
                description='longer description',
                value=...
            ),
            ...
        ],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class CreateAfterBeforePrayer(generics.CreateAPIView):
    """
    endpoint to create after before prayer hooks 
    """
    authentication_classes=(TokenAuthentication,)
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = AfterBeforePrayerSerializer
    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            AfterBeforePrayerSerializer,
        ],
        # override default docstring extraction
        description='More descriptive text',
        # provide Authentication class that deviates from the views default
        auth=TokenAuthentication,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
        # attach request/response examples to the operation.
        examples=[
            OpenApiExample(
                'Example 1',
                description='longer description',
                value=...
            ),
            ...
        ],
    )
    def create(self, request, *args, **kwargs):
        data=request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        PrayerEvent.objects.create(user=request.user,type=data.get("type"),prayer=data.get("prayer"),repeated=data.get("repeated"),audio=data.get("audio"),)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class CurrentPrayerTime(APIView):
    """
    View to get current prayer time 
    * Requires token authentication.
    * Only auth users are able to access this view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(description='adan Login api ', methods=["get"],parameters=[TokenSerializer],responses=(PrayerSerializer),)
    def get(self, request, format=None):
        """
        Return a current day prayer time 
        """
        self_user = request.user
        self_mosque = Mosque.objects.filter(topic=self_user).first()
        print(self_mosque)
        current_date_mounth = datetime.today().month
        current_date_day = datetime.today().day
        id_day = (current_date_mounth-1)*30+current_date_day # get current day id 
        prayer_json =self_mosque.state.prayer_time["data"][id_day]
        adan_json={
        "adan_elfajer" : PrayerAudio.objects.filter(prayer="elfajer").last().audio.url,
        "adan_duhr" : PrayerAudio.objects.filter(prayer="duhr").last().audio.url,
        "adan_alasr" : PrayerAudio.objects.filter(prayer="alasr").last().audio.url,
        "adan_almaghreb" : PrayerAudio.objects.filter(prayer="almaghreb").last().audio.url,
        "adan_alaicha" : PrayerAudio.objects.filter(prayer="alaicha").last().audio.url
        }
        return Response({"mosque_name":self_mosque.name,"time":prayer_json,"adan":adan_json})
class CurrentMosqueState(APIView):
    """
    View to get current mosque connection state  
    * Requires token authentication.
    * Only auth users are able to access this view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(description='mosque status', methods=["get"],parameters=[TokenSerializer],responses=(StatusSerializer),)

    def get(self, request, format=None):
        """
        Return a current mosque connection state
        """
        current_user = request.user
        try:
            self_mosque = Mosque.objects.get(topic=current_user)
            return Response({"status":self_mosque.status})
        except:
            self_mosque=None
            return Response({"error":"Unauthorized"},status=status.HTTP_401_UNAUTHORIZED)

class CreatePrayerAdan(generics.CreateAPIView):
    """
    endpoint to create prayer adan ['elfajer','duhr','alasr','almaghreb','alaicha']
    """
    authentication_classes=(TokenAuthentication,)
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = PrayerAdanSerializer
    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            PrayerAdanSerializer,
        ],
        # override default docstring extraction
        description='More descriptive text',
        # provide Authentication class that deviates from the views default
        auth=TokenAuthentication,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
        # attach request/response examples to the operation.
        examples=[
            OpenApiExample(
                'Example 1',
                description='longer description',
                value=...
            ),
            ...
        ],
    )
    def create(self, request, *args, **kwargs):
        data=request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        PrayerEvent.objects.create(user=request.user,type=data.get("type"),prayer=data.get("prayer"),repeated=data.get("repeated"),audio=data.get("audio"),)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)