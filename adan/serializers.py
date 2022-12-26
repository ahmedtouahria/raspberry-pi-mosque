from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

class LiveAudioSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model=LiveEvent
        fields="__all__"
        read_only_fields=('audio_duration',)
class PrayerAdanSerializer(serializers.ModelSerializer):
    class Meta:
        model=PrayerAudio
        fields="__all__"
        read_only_fields=('audio_duration',)

class AfterBeforePrayerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model=PrayerEvent
        fields="__all__"
        read_only_fields = ['user','audio_duration']
class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Incorrect username or password')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
class PrayerSerializer(serializers.Serializer):
    elfajer = serializers.TimeField(
        label=_("elfajer"),
        read_only=True

    )
    duhr = serializers.TimeField(
        label=_("duhr"),
        read_only=True

    )
    alasr = serializers.TimeField(
        label=_("alasr"),
        read_only=True
    )
    almaghreb = serializers.TimeField(
        label=_("almaghreb"),
        read_only=True
    )
    alaicha = serializers.TimeField(
        label=_("alaicha"),
        read_only=True
    )

class TokenSerializer(serializers.Serializer):
    authorization = serializers.CharField(
        label=_("Authorization"),
        write_only=True
    )
