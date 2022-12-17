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
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        print(request.user)
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
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a current day prayer time 
        """
        current_date_mounth = datetime.today().month
        current_date_day = datetime.today().day
        id_day = (current_date_mounth-1)*30+current_date_day
        prayer_json =json.loads(config.PRAYER_SOURCE)["data"][id_day]
        print(id_day)
        return Response(prayer_json)

class CurrentMosqueState(APIView):
    """
    View to get current mosque connection state  
    * Requires token authentication.
    * Only auth users are able to access this view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a current mosque connection state
        """
        current_user = request.user
        try:
            self_mosque = Mosque.objects.get(user=current_user)
            return Response({"mosque":self_mosque.status})
        except:
            self_mosque=None
            return Response({"error":"Unauthorized"},status=status.HTTP_401_UNAUTHORIZED)

