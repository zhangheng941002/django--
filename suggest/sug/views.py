from django.shortcuts import render, redirect
from django.http import HttpResponse
from user.models import *
from user.islogin import islogin
from sug.models import *

from sug.send_email import send_email

from sug.isquanxian import isquanxian
from django.core.paginator import Paginator  # 用于分页显示


def chuli(request):
    # 通过隐藏传过来的ycid,获取创意详情
    id = request.POST.get('ycid')
    # 获得发布创意的详细内容
    sug_content = Sug.objects.get(id=id).content
    # 获得创意的发布者
    sug_name = Sug.objects.get(id=id).uname
    # 获得创意发布的id
    sug_id = Sug.objects.get(id=id).id

    # 获得创意的类型
    sug_lx = Sug.objects.get(id=id).fl

    # 获得指定处理人的信息
    clr = Clpeople.objects.filter(cylx=sug_lx)

    if request.method == "POST":
        return render(request, 'sug/chuli.html',
                      {'clr': clr, 'sug_content': sug_content, 'sug_name': sug_name, 'sug_id': sug_id})


@isquanxian
def look_sfsl(request, pageindex):
    # 接受跳转输入的页数
    input_page = request.GET.get("input_page")
    if input_page:
        pageindex = int(input_page)
    if pageindex == '':
        pageindex = '1'

    # 查询所有的创意,这里展示就把最先提交的展示在最前面
    list1 = Sug.objects.filter(is_sl=False)  # .order_by('-id')  倒叙
    # 创建一个paginator对象
    paginator = Paginator(list1, 10)

    # 获取最后一页的页码
    last_page = len(paginator.page_range)

    if int(pageindex) > last_page:
        pageindex = last_page

    if int(pageindex) <= 0:
        pageindex = 1

    page = paginator.page(int(pageindex))

    return render(request, 'sug/show_info.html', {'page': page, 'last': last_page})


# 展示每个创意的详细信息
def show_info(request, id):
    title = id
    # 查找创意的对象
    sug = Sug.objects.get(id=int(id))
    return render(request, 'dl_every_info.html', {"sug": sug})


# 接受处理后结果的视图
def result(request):
    """
    处理完，还要去数据库标记，改为True,两个字段
    如果采纳则发给执行人
    不管采纳不采纳都发给创意申请人，告知结果
    """
    # 获取是否采纳
    sfcn = request.POST.get('cl')

    # 获取意见详情,用于发送给发布着
    yjxq = request.POST.get('yjxq')

    # 获取管理员信息，用于发送邮件
    username = request.session.get('username')

    # 获取管理员邮箱
    man_email = User.objects.get(username=username).email

    # 获取管理员邮箱授权码
    man = Man.objects.get(name=username)
    man_sqm = man.sqm

    # 获取创意提交者的邮箱
    put_cy = request.POST.get("tjr")
    tjr_email = User.objects.get(username=put_cy).email

    # 修改该创意是否浏览的状态
    sug_id = request.POST.get("sug_id")
    sug1 = Sug.objects.get(id=sug_id)
    # 修改浏览状态
    sug1.is_sl = True

    # 修改数据中user_sug表格中的 sl 字段 ,一开始盖子段为空，如果采纳则改为1，没有采纳改为0
    # 如果采纳，则传给指定人执行,采纳过来的是创意的等级，用于后期发奖金
    if sfcn == "A" or sfcn == "B" or sfcn == "C" or sfcn == "D":
        sug1.sl = True
        # 获取管理员指定的处理人
        clr = request.POST.get("clr")
        # 查询处理人的邮箱
        clr_email = User.objects.get(username=clr).email
        sug1.zxr = clr

        # 创建邮箱内容，把发布者的创意告诉告诉执行人，让其处理
        sug_content = request.POST.get("sug_content")

        # 把邮件发送给处理人
        res = send_email(man_email, man_sqm, clr_email, sug_content)
        # 发送邮件给创意的发布者，告诉创意已经采纳，并由谁执行
        res = send_email(man_email, man_sqm, tjr_email, "你的创意已经采纳，正在由%s 执行" % clr)

        # 这里采纳了，就有创意等级，再次进行积分处理，这里A的等级最高，积分最高，A，B，C，D对应积分为4，3，2，1
        user1 = User.objects.get(username=put_cy)

        if sfcn == 'A':
            user1.jf += 4
            sug1.dj = 'A'
        if sfcn == 'B':
            user1.jf += 3
            sug1.dj = 'B'
        if sfcn == 'C':
            user1.jf += 2
            sug1.dj = 'C'
        if sfcn == 'D':
            user1.jf += 1
            sug1.dj = 'D'
        user1.save()


    # 没被采纳，告诉发布者
    else:
        sug1.sl = False
        # 发送邮件给创意发布者，告诉他是否受理其创意
        res = send_email(man_email, man_sqm, tjr_email, "你的创意未被采纳，请再接再厉")

    sug1.save()

    return render(request, 'sug/clcg.html')
