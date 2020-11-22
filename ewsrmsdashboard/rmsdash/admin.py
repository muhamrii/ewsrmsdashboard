from django.contrib import admin

from .models import DbReport
from .models import TbServer
# Register your models here.

class DbReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'botid', 'groupid')

class TbServerAdmin(admin.ModelAdmin):
    list_display = ('servername','ipaddress','username','port')

admin.site.register(DbReport, DbReportAdmin)
admin.site.register(TbServer, TbServerAdmin)
