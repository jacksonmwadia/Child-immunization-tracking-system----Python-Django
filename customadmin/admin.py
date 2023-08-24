from django.contrib import admin
from .models import County, Hospital


class CountyAdmin(admin.ModelAdmin):
    list_display = ['name', 'county_no']
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(County, CountyAdmin)

class HospitalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'county', 'date_created']
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Hospital, HospitalAdmin)