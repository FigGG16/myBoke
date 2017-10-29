from django.db import models
from datetime import datetime
# Create your models here.
#导入django的user表
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractBaseUser


#用户个人信息,继承AbstractUser，覆盖django默认的user
class UserProfile(AbstractUser):
     nick_name = models.CharField(max_length=50,verbose_name=u"昵称",default=" ")
     birday = models.DateField(verbose_name=u"生日",null=True,blank=True)
     gender=models.CharField(choices=(("male",u"男") ,("female","女")),default="female",max_length=7)
     address=models.CharField(max_length=100,default=u"")
     mobile = models.CharField(max_length=11,null=True,blank=True)
     image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png",max_length=100)
     #配置表的Meta信息
     class Meta:
         verbose_name="用户信息"
         verbose_name_plural=verbose_name
     #重载unicode方法，防止print的时候不能打印字符串
     def __str__(self):
         return self.username

#邮箱模型
class EmailVerifyRecord(models.Model):
 #以下两个都不能为空
     code = models.CharField(max_length=20,verbose_name=u"验证码")
     email=models.EmailField(max_length=50,verbose_name=u"邮箱")

     #找回密码时的验证码
     send_type = models.CharField(choices=(("register",u"注册") ,("forget",u"找回密码")),max_length=10)
     send_time = models.DateTimeField(default=datetime.now)
     is_useful=models.BooleanField(default=True)

     class Meta:
         verbose_name=u"邮箱验证码"
         verbose_name_plural=verbose_name

#轮播图
class Banner(models.Model):
     title= models.CharField(max_length=100,verbose_name="标题")
     image=models.ImageField(upload_to="banner/%Y/%m",verbose_name=u"轮播图",max_length=100)
     url = models.URLField(max_length=200,verbose_name=u"访问地址")
     index = models.IntegerField(default=100,verbose_name=u"顺序")
     add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

     class Meta:
         verbose_name = u"轮播图"
         verbose_name_plural=verbose_name