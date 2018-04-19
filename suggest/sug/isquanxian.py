from django.shortcuts import redirect,render
from django.http import HttpResponseRedirect
from sug.models import *
#如果点击需要管理员才能进的页面，来在验证是否有权限
def isquanxian(func):
    def login_fun(request,*args,**kwargs):
        username = request.session.get('username')
        # 获取管理员,有权限则可以编辑
        if Man.objects.filter(name=username):
            return func(request,*args,**kwargs)
        # 没有权限，返回个人中心
        else:
            # return redirect('/user/ucenter')
            return render(request,'sug/noquanxian.html')
    return login_fun