from django.contrib import admin
from .models import *
# Register your models here.


class LiveEventAdmin(admin.ModelAdmin):
    model = LiveEvent
    readonly_fields=('audio_duration',)
    list_display=("name","user",'created_at','audio_duration')
class PrayerAudioAdmin(admin.ModelAdmin):
    model = PrayerAudio
    readonly_fields=('audio_duration',)
class PlugTabular(admin.StackedInline):
    model=Plug
class MosqueAdmin(admin.ModelAdmin):
    model=Mosque
    inlines=[PlugTabular,]
    list_display=("name","status",'state',"speaker_status")
    readonly_fields=("status",)
admin.site.register(LiveEvent,LiveEventAdmin)
admin.site.register(State)
admin.site.register(PrayerEvent)
admin.site.register(Mosque,MosqueAdmin)
admin.site.register(Topic)
admin.site.register(Plug)
admin.site.register(PrayerAudio,PrayerAudioAdmin)


