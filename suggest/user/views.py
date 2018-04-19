from django.shortcuts import render, redirect
from django.conf import settings
from user.models import *
from django.core.paginator import Paginator  # 用于分页显示
import os
from suggest.views import shouye
# 用于限制个人中心等的在登陆状态才能访问
from user.islogin import islogin

from django.http import JsonResponse


# 生成验证码
def yanzhengma(request):
    import random
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0qwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # return  rand_str
    request.session['rand_str'] = rand_str
    return JsonResponse({'st': rand_str})


# 登陆
def login(request):
    # 设置关闭浏览器 session 就失效，即关闭浏览器，不管用户是否推出都推出登陆
    request.session.set_expiry(0)

    if request.method == "GET":
        return render(request, 'user/login.html')
    # form 表单post请求过来的

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 通过获得的username 和 password 跟数据库进行匹配
        if User.objects.filter(username=username, password=password):
            # 验证通过，转到个人中心,并保存session,用于验证用户是否登陆
            request.session['username'] = username
            username = request.session.get('username')
            user = User.objects.get(username=username)
            uid = user.id
            request.session['id'] = uid
            put_url = request.COOKIES.get('url')

            return render(request, 'shouye_dl.html')

        else:
            # 验证不通过，重新渲染登陆页面
            if User.objects.filter(username=username):
                # 密码错误
                return render(request, 'user/login.html', {'ps': "用户名或密码不正确", 'un': username})


# 退出登陆
def logout(request):
    request.session.flush()

    return redirect(shouye)


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    # 是post请求那说明是从form表单中来的注册数据，进行数据库的用户插入
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        # 后台的再次验证密码是防止黑客的，因为浏览器来的数据都是不可信的，因为这里是毕设就弄的复杂了，我们就默认浏览器来的数据是安全的
        if password != password2:
            return render(request, 'eyizhuce.html')

        # 验证邮箱是否存在
        elif User.objects.filter(email=email):
            return render(request, 'user/register.html', {'ema': '邮箱已存在'})

        u1 = User(username=username, password=password, email=email)
        u1.save()
        # 注册成功后，跳到登陆页面,
        return render(request, 'user/success.html')


# 验证用户名是否存在
def register_exist(requset):
    uname = requset.GET.get('uname')
    count = User.objects.filter(username=uname).count()
    print(count)
    return JsonResponse({'count': count})


# 个人中心
@islogin
def ucenter(request, pageindex):
    # 接受跳转输入的页数
    input_page = request.GET.get("input_page")
    # print(input_page)
    if input_page:
        pageindex = int(input_page)

    uid = request.session.get('id')
    if pageindex == '':
        pageindex = '1'
    # 查询所有的创意
    list1 = Sug.objects.filter(uid=uid).order_by('-id')
    # 创建一个paginator对象
    paginator = Paginator(list1, 10)

    # 获取最后一页的页码
    last_page = len(paginator.page_range)

    # 控制页面跳转时，用户的输入，<= 0 为第一页，>最大页，为最大页
    if int(pageindex) > last_page:
        pageindex = last_page

    if int(pageindex) <= 0:
        pageindex = 1

    page = paginator.page(int(pageindex))

    username = request.session.get('username')

    return render(request, 'user/shouye_denglu.html', {'page': page, 'last': last_page, 'username': username})


# 用户提交的建议处理,放在数据库里，并重定向到用户中心
@islogin
def selove_sug(request):
    if request.method == "POST":
        # 创意分类
        fl = request.POST.get('fl')
        # 标题
        title = request.POST.get("title")
        # 内容
        content = request.POST.get('content')

        # 通过session 中存的username 查找id,获取user对象,用于外键关联
        username = request.session.get('username')
        user = User.objects.get(username=username)
        uname = user.username

        # 附件名字存储，跟id 绑定
        now_last = Sug.objects.all().order_by('-id')[0].id
        filename = now_last + 1

        try:
            # 上传的附件保存到服务器
            f1 = request.FILES['fujian']
            # print(fl)

            # 获取附件文件格式
            houzhui = f1.name.split('.')[1]

            fn = str(filename) + "." + houzhui
            fname = os.path.join(settings.MEDIA_ROOT, fn)
            # 保存
            with open(fname, 'wb') as f:
                for c in f1.chunks():
                    f.write(c)
        except:
            fn = ''
        sug1 = Sug(filename=fn, fl=fl, title=title, uname=uname, content=content, uid=user)
        sug1.save()

        # 把提交的优化存入数据库后，渲染提交成功的页面
        return render(request, 'sug/sug_success.html')


# 发起合理化创意
@islogin
def push_sug(request):
    return render(request, 'user/youhua.html')


"""
1、展示总积分，和应得的奖金
2、你被采纳的创意，及其获得的等级
"""


@islogin
def jifen(request, pageindex):
    # 接受跳转输入的页数
    input_page = request.GET.get("input_page")
    if input_page:
        pageindex = int(input_page)

    uid = request.session.get('id')
    if pageindex == '':
        pageindex = '1'
    # 查询采纳的创意
    list1 = Sug.objects.filter(uid=uid).filter(sl='True').order_by('-id')
    # 创建一个paginator对象
    paginator = Paginator(list1, 10)

    # 获取最后一页的页码
    last_page = len(paginator.page_range)

    if int(pageindex) > last_page:
        pageindex = last_page
    if int(pageindex) <= 0:
        pageindex = 1
    page = paginator.page(int(pageindex))

    # 获取用户的积分
    id = request.session.get('id')
    user = User.objects.get(id=id)
    jf = user.jf
    # 根据积分结算奖金，一积分奖励10元
    jj = jf * 10

    return render(request, 'user/jifenzhongxin.html', {'page': page, 'last': last_page, 'jf': jf, 'jj': jj})


# 如果有附件，则下载
def load(request):
    # 获取附件的名字
    name = request.GET.get("ld")
    page = name.split('.')[0]

    # 服务器中附件的地址
    path = settings.MEDIA_ROOT + name

    # 保存地址，如果你想修改，这这个地方,改 pat
    pat = 'F:\图片' + "/" + name

    c = open(path, 'rb').read()
    with open(pat, 'wb') as f:
        f.write(c)
    return redirect('/sug/show_info' + "/" + page)


# 修改密码
def xgmm(request):
    if request.method == 'GET':
        return render(request, 'user/xgmm.html')
    if request.method == "POST":
        pwd = request.POST.get('newpwd')
        uname = request.session.get('username')
        user = User.objects.get(username=uname)
        user.password = pwd

        print(user.password)
        print(pwd)
        user.save()
        request.session.flush()
        # 提醒修改成功，渲染页面
        return render(request, 'user/xgmm_cg.html')
