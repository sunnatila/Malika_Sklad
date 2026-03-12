from django.contrib import admin
from .models import Battery, Charger, Display, Brand


@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'watt', 'voltage', 'capacity', 'count')


@admin.register(Charger)
class ChargerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'watt', 'voltage', 'count')


@admin.register(Display)
class DisplayAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'hz', 'pin', 'count')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
