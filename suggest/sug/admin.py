from django.contrib import admin

from sug.models import *


class ClpeopleAdmin(admin.ModelAdmin):
    # 后台展示的字段,展示标题，分类，谁提交的
    list_display = ['clr_name', 'cylx']
    # 每页显示几条
    list_per_page = 10


class ManAdmin(admin.ModelAdmin):
    # 后台展示的字段
    list_display = ['name','sqm']
    list_per_page = 10


admin.site.register(Clpeople,ClpeopleAdmin)
admin.site.register(Man,ManAdmin)
