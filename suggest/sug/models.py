from django.db import models


# 这里的两个模型类，用来生成表，而表中的数据跟你的需要，后天管理者自己添加即可

# 这个表是创意的执行人的表格，这里 你把需要的执行人的名字填到这个表中即可
class Clpeople(models.Model):
    clr_name = models.CharField(max_length=20,verbose_name='执行者',db_column='clr_name')
    cylx = models.CharField(max_length=20,verbose_name="处理的创意类型",db_column='cylx')


# 审核的管理员模型类，这里只是用来在数据库中生成表，如果需要管理员，这里你把用户的姓名，和获取的邮箱的授权码填到这个表中即可
class Man(models.Model):

    # verbose_name='名字' 这个是在admin 管理中显示的中文字段名字
    name = models.CharField(max_length=20,verbose_name='名字',db_column='name')
    sqm = models.CharField(max_length=20,verbose_name='邮箱授权码',db_column='sqm')
