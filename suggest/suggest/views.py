# 人丑就要多学习
from django.shortcuts import render, redirect
from django.core.paginator import Paginator  # 用于分页显示
from user.models import *


# 分页显示,这里是之前用于首页展示的，按照你的要求去掉了，我没用这里
def page(request, pageindex):
    # 接受跳转输入的页数
    input_page = request.GET.get("input_page")
    if input_page:
        pageindex = int(input_page)
    if pageindex == '':
        pageindex = '1'

    # 查询所有的创意
    list1 = Sug.objects.all().order_by("-id")
    # 创建一个paginator对象
    paginator = Paginator(list1, 10)

    # 获取最后一页的页码
    last_page = len(paginator.page_range)

    if int(pageindex) > last_page:
        pageindex = last_page

    if int(pageindex) <= 0:
        pageindex = 1

    page = paginator.page(int(pageindex))

    uid = request.session.get('id')
    if uid:
        # 如果登陆渲染登陆模版
        return render(request, 'user/person_centen_denglu.html', {'page': page, 'last': last_page})
    else:
        # 如果没有uid 说明没有登陆，渲染未登录的模版
        return render(request, 'user/person_centen_nodl.html', {'page': page, 'last': last_page})


# 首页
def shouye(request):
    return render(request, 'shouye.html')


# 搜索
def sousuo(request):
    uid = request.session.get('id')
    if uid:
        # 如果登陆渲染登陆模版
        return render(request, 'sousuo_denglu.html')
    else:
        # 如果没有uid 说明没有登陆，渲染未登录的模版
        return render(request, 'sousuo_nodl.html')


# 展示每个创意的详细信息
def show_info(request, id):
    title = id

    # 查找创意的对象
    sug = Sug.objects.get(id=int(id))
    # print(sug.title)
    return render(request, 'every_info.html', {"sug": sug})


# 查询
def select(request, pageindex):
    # 接受跳转输入的页数
    input_page = request.GET.get("input_page")

    if input_page:
        pageindex = int(input_page)
    if pageindex == '':
        pageindex = '1'

    # 如果是通过搜素来的查询结果，则是POST请求
    if request.method == 'POST':
        # 获取前面获取的要查询的，传来的是分类名称，
        fl_name = request.POST.get('flxx')  # 通过前段出来来的 name 属性获取
        # print(fl_name)
        list1 = Sug.objects.filter(fl=fl_name).order_by('-id')
        # 统计有多少条创意
        count = Sug.objects.filter(fl=fl_name).count()
        # 统计有多少条创意被采纳
        cn_count = Sug.objects.filter(fl=fl_name, sl=True).count()

        # 创建一个paginator对象
        paginator = Paginator(list1, 10)

        # 获取最后一页的页码
        last_page = len(paginator.page_range)

        if int(pageindex) > last_page:
            pageindex = last_page

        if int(pageindex) <= 0:
            pageindex = 1

        page = paginator.page(int(pageindex))

        # 把搜索字段存入session 用于翻页中的查询
        request.session['ss'] = fl_name

    fl_name = request.session.get('ss')
    # 通过输入页码过来的，是GET请求
    if request.method == "GET":
        list1 = Sug.objects.filter(fl=fl_name).order_by('-id')
        # 统计有多少条创意
        count = Sug.objects.filter(fl=fl_name).count()
        # 统计有多少条创意被采纳
        cn_count = Sug.objects.filter(fl=fl_name, sl=True).count()

        # 创建一个paginator对象
        paginator = Paginator(list1, 10)

        # 获取最后一页的页码
        last_page = len(paginator.page_range)

        if int(pageindex) > last_page:
            pageindex = last_page

        if int(pageindex) <= 0:
            pageindex = 1

        page = paginator.page(int(pageindex))

    uid = request.session.get('id')
    if uid:
        # 如果登陆渲染登陆模版
        return render(request, 'user/cx_denglu.html',
                      {'page': page, 'last': last_page, 'count': count, 'cn_count': cn_count})
    else:
        # 如果没有uid 说明没有登陆，渲染未登录的模版
        return render(request, 'user/cx_nodl.html',
                      {'page': page, 'last': last_page, 'count': count, 'cn_count': cn_count})
