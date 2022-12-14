from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
#routers.register(r'live_event', LiveEventView, basename='matchs_reserved')

urlpatterns = [
    path('',include(routers.urls)), 
    path('create_live_event',LiveEventView.as_view())
]
