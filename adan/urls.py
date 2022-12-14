from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
#routers.register(r'live_event', LiveEventView, basename='matchs_reserved')

urlpatterns = [
    path('',include(routers.urls)),
    path('login/', LoginView.as_view(), name='knox_login'),# login user
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path("current_today_prayer_time/", CurrentPrayerTime.as_view()),
    path("current_mosque_status/", CurrentMosqueState.as_view()),
    path("add_prayer_event/", CreateAfterBeforePrayer.as_view()),
    path('create_live_event/',LiveEventView.as_view()),
    path('create_prayer_adan/',CreatePrayerAdan.as_view()),
    path('turn_on_off/',TurnOnOffSpeaker.as_view())

]
