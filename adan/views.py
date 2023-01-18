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
                prayer_json =self_mosque.state.prayer_time["data"][id_day]
                print(prayer_json)
            except Exception as e:
                return Response({"success":False,"error":e})
            return Response({"mosque_name":self_mosque.name,"time":prayer_json,})
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
        command = request.data.get('command')
        print(command)
        return Response({"success":True,"data":command},status=status.HTTP_200_OK)
    @extend_schema(description='get turn on off command', methods=["get"],parameters=[TokenSerializer],responses=(TurnOnOffSerializer))
    def get(self,request,format=None):
        return Response({"command":True},status=status.HTTP_200_OK)