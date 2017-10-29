__author__ = 'FigGG'
__date__ = '2017/8/1 下午11:21'

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    #判断密码是否存在，指定长度
    username=forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class LoginCaptch(forms.Form):
    captcha = CaptchaField()

class RegisterForm(forms.Form):
    email= forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

#
#找回密码
class ForgetForm(forms.Form):
    email= forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})
    # 再去views里实例化

#修改密码view
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)