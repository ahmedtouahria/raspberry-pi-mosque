from .serializers import *
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
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
        serializer.save(user=request.user)
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
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
from hijri_converter import Gregorian,Hijri
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
        * Return a current day prayer time 
        """
        self_topic = request.user.topic
        try:
            self_mosque = Mosque.objects.get(topic=self_topic)
        except:
            self_mosque=None
        if self_mosque:
            current_date_mounth = datetime.today().month
            current_date_day = datetime.today().day
            id_day = (current_date_mounth-1)*30+current_date_day # get current day id
            try: 
                prayer_json =self_mosque.state.prayer_time_am_pm["data"][id_day]
                prayer_json_without_pm =self_mosque.state.prayer_time["data"][id_day]
                current_time = datetime.now().time()
                elfajer_time = datetime.strptime(prayer_json_without_pm["elfajer"],"%H:%M:%S")
                duhr_time = datetime.strptime(prayer_json_without_pm["duhr"],"%H:%M:%S")
                alasr_time = datetime.strptime(prayer_json_without_pm["alasr"],"%H:%M:%S")
                almghreb_time = datetime.strptime(prayer_json_without_pm["almaghreb"],"%H:%M:%S")
                alaicha_time = datetime.strptime(prayer_json_without_pm["alaicha"],"%H:%M:%S")
                from .utils import get_time_near_prayer,get_total_seconds
                time_now_seconds = current_time.hour*3600+current_time.minute*60+current_time.second
                remaining = get_time_near_prayer(date_now_seconds=time_now_seconds,elfajer=elfajer_time,duhr=duhr_time,alasr=alasr_time,
                almaghreb=almghreb_time,alaicha=alaicha_time
                )
                prayer_detect_time = datetime.strptime(prayer_json_without_pm[f"{remaining[1]}"],"%H:%M:%S")
                prayer_detect_time_seconds = get_total_seconds(prayer_detect_time)
                status = "-"
                if prayer_detect_time_seconds-time_now_seconds<0:
                    status="+"
                else:
                    status="-"
                date_today = datetime.today()
                milad_date=hijri_date = Gregorian(date_today.year,date_today.month,date_today.day)
                hijri_date = milad_date.to_hijri()
                hijri_date_ar = Hijri(hijri_date.year,hijri_date.month,hijri_date.day)
                hijri_date_display = f" {hijri_date_ar.day_name('ar')} - {hijri_date.day}  {hijri_date_ar.month_name('ar')} - {hijri_date.year}"
                miladi_date_display = f"{milad_date.day_name('ar')} {date_today.day} {milad_date.month_name('ar')} {date_today.year}"
            except Exception as e:
                return Response({"success":False,"error":str(e)})
            return Response({"mosque_name":self_mosque.name,"time":prayer_json,"day_hijri":hijri_date_display,"miladi_date":miladi_date_display,"remaining":f'{status}{remaining[0]}',"near_prayer":remaining[1]})
        else:
            return Response({"success":False,"message":"your mosque not linked with your account"})
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
        import requests
        BASE_URL=config.BASE_MQTT_API_URL
        username=config.MQTT_USERNAME
        password=config.MQTT_PASSWORD
        current_user = request.user
        try:
            topic = Topic.objects.get(user=current_user)
        except Topic.DoesNotExist:
            topic=None
        if topic:
                response = requests.get(f'{BASE_URL}/clients/{topic.serial_number}', auth=(username, password))
                print(topic.serial_number)
                print(json.loads(response.text))
                response_dict = json.loads(response.text)
                try:
                    if response_dict['connected']:
                        return Response({"status":True})
                    else:
                        return Response({"status":False})
                except:
                    return Response({"status":False,"message":response_dict})
        else: return Response({"success":False,"message":'Topic id does not exist'})

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
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes=(permissions.IsAuthenticated,)
    @extend_schema(description='logout api', methods=["post"],parameters=[TokenSerializer],responses=(LogoutSerializer),)

    def post(self, request, format=None):
        from django.contrib.auth.signals import user_logged_in, user_logged_out
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response({"sucess":True,"message":"user logout successfully"}, status=status.HTTP_200_OK)

class TurnOnOffSpeaker(APIView):
    authentication_classes=[TokenAuthentication]
    @extend_schema(description='turn on off command', methods=["post"],parameters=[TokenSerializer],responses=(TurnOnOffSerializer),request=TurnOnOffSerializer)
    def post(self,request,format=None):
        command = request.data.get('command',None)
        if command:
            return Response({"success":True,"data":{"command":True}},status=status.HTTP_200_OK)
        else: return Response({"success":False,"message":"command must be not null"},status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(description='get turn on off command', methods=["get"],parameters=[TokenSerializer],responses=(TurnOnOffSerializer))
    def get(self,request,format=None):
        return Response({"command":True},status=status.HTTP_200_OK)