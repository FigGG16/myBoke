__author__ = 'FigGG'
__date__ = '2017/8/3 上午1:47'

from random import Random
from django.shortcuts import render
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from myBoke.settings import EMAIL_FROM

#随机数
def random_str(randomllength=8):
    str = ''
    chars ='AaBbCcDdEeFfGHhIiJjKkgOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomllength):
        str+=chars[random.randint(0,length)]
    return str

#事先把要发送的code保存在数据库当中
def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    code=random_str(16)
    email_record.code = code
    email_record.is_useful=1
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type =="register":
        email_title="飞翔博客注册链接"
        email_body = "请点击下链接进行激活：http://127.0.0.1:8001/active/{0}".format(code)
        #
        #在setting中配置发送者的SMTP服务器
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            #然后在views里添加
            pass


    elif send_type =="forget":
        email_title = "飞翔博客密码重置链接"
        email_body = "请点击下链接进行重置：http://127.0.0.1:8001/reset/{0}".format(code)
        #
        # 在setting中配置发送者的SMTP服务器
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            # 然后在views里添加
            pass