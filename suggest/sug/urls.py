# 人丑就要多学习
from django.conf.urls import url
from sug.views import *
urlpatterns = [
    url(r'^chuli/$', chuli),
    url(r'look_sfsl/(\d*)$',look_sfsl),
    url(r'show_info/(\d+)/',show_info),
    url(r'result/',result),




]