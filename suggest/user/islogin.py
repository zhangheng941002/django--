
from django.http import HttpResponseRedirect

#如果登录则转到登录页面
def islogin(func):
    def login_fun(request,*args,**kwargs):
        if request.session.get('username'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url',request.path)
            red.set_cookie('cen','/user/ucenter')
            return red
    return login_fun