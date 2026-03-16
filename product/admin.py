from django.contrib import admin
from .models import Battery, Charger, Display


@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'model_name', 'count')


@admin.register(Charger)
class ChargerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'watt', 'voltage', 'count')


@admin.register(Display)
class DisplayAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'hz', 'pin', 'count')
