from django.contrib import admin
from .models import Keycard, AccessLog

@admin.register(Keycard)
class KeycardAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'uid', 'is_active')

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'scanned_uid', 'granted')
    list_filter = ('granted',)
