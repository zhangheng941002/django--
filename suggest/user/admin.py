from django.contrib import admin

from user.models import *

# class SugAdmin(admin.ModelAdmin):
#     # 后台展示的字段,展示标题，分类，谁提交的
#     list_display = ['title', 'fl', 'uname']
#     # 每页显示几条
#     list_per_page = 10
#
#
# class UserAdmin(admin.ModelAdmin):
#     # 后台展示的在等
#     list_display = ['username', 'password']
#
#     list_per_page = 10
#
#
# admin.site.register(User, UserAdmin)
# admin.site.register(Sug, SugAdmin)
