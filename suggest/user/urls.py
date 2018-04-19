# 人丑就要多学习

from django.conf.urls import url
from user.views import *

urlpatterns = [
    url(r'^login/$', login),
    url(r'^register/$', register),
    url(r'^ucenter/(\d*)$', ucenter),
    url(r'^logout/$', logout),
    url(r'^selove_sug/$', selove_sug),
    url(r'^push_sug$', push_sug),
    url(r'^jifen/(\d*)$', jifen),
    url(r'^load/$', load),
    url(r'^register_exist/$', register_exist),
    url(r'^yanzhengma/$', yanzhengma),
    url(r'^xgmm/$', xgmm)

]
