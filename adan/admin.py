from django.contrib import admin
from .models import *
# Register your models here.


class LiveEventAdmin(admin.ModelAdmin):
    model = LiveEvent
    readonly_fields=('audio_duration',)

class PrayerAudioAdmin(admin.ModelAdmin):
    model = PrayerAudio
    readonly_fields=('audio_duration',)

admin.site.register(LiveEvent,LiveEventAdmin)
admin.site.register(State)
admin.site.register(PrayerEvent)
admin.site.register(Mosque)
admin.site.register(PrayerAudio,PrayerAudioAdmin)


