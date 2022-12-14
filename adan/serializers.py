from rest_framework import serializers
from .models import *
class LiveAudioSerializers(serializers.ModelSerializer):
    class Meta:
        model=LiveEvent
        fields="__all__"