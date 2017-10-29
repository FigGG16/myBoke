from django.shortcuts import render
#处理邮箱登录
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View

#数据库搜索时的"并"语法
from django.db.models import Q
# Create your views here.
from .models import UserProfile

from .forms import LoginForm

#处理用户登录
from django.contrib.auth import authenticate,login,logout


#处理验证码
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password
from users.utils.email_send import send_register_email

#邮箱验证模型
from .models import EmailVerifyRecord

# from .forms import ForgetForm

from .forms import LoginCaptch,ForgetForm,ModifyPwdForm

#用户登出
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect



class CustomBackend(ModelBackend):
    # 通过自定义auth完善邮箱(和用户名)登录
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                 return user
        except Exception as e:
            return None

#用户登录验证
# def user_login(request):
#     #判断是否为POST请求
#     if request.method =="POST":
#         #获取用户名和密码
#         user_name=request.POST['username']
#         pass_word=request.POST['password']
#
#         #验证用户名和密码是否正确，返回TRUE/FASLE
#         user = authenticate(username=user_name,password=pass_word)
#
#         if user is not None:
#             login(request,user)
#             return render(request,"login.html")
#         else:
#             return render(request,"login.html",{})
#         pass
#     elif request.method =="GET":
#         return render(request,"login.html",{})


class LoginView(View):
    # 登录的View
    def get(self,request):
        loginCaptch = LoginCaptch()
        return render(request,"login.html",{'loginCaptch':loginCaptch})

    def post(self,request):
        #加载验证码
        loginCaptch = LoginCaptch()
        # 声明一个form实例
        login_form =LoginForm(request.POST)

        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']

            # 验证用户名和密码是否正确，返回TRUE/FASLE
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户名未激活",'loginCaptch':loginCaptch,'login_form':login_form})

            else:
                return render(request,"login.html",{"msg": "用户名或密码错误",'loginCaptch':loginCaptch,'login_form':login_form})

        else:
            return render(request, "login.html", {'login_form':login_form,'loginCaptch':loginCaptch})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))



class ActiveUserView(View):
    # 激活
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                if record.is_useful:
                    email = record.email
                    user = UserProfile.objects.get(email = email)
                    user.is_active = True
                    #在 LoginView 添加判断user.is_active:才能登录
                    user.save()

                    # 验证完后取消验证链接
                    EmailVerifyModeLl = EmailVerifyRecord.objects.get(code=active_code)
                    EmailVerifyModeLl.is_useful = False
                    EmailVerifyModeLl.save()
                else:
                    return render(request, "login.html", {'msg': "验证码过期"})

        else:
            return render(request,"active_fail.html")
        return render(request, "login.html")



class RegisterView(View):
    # 注册View
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{'register_form':register_form})

    def post(self,request):

        register_from = RegisterForm(request.POST)

        if register_from.is_valid():
            user_name = request.POST['email']
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_from, "msg": "用户已经存在"})
            pass_word = request.POST['password']
            pass_word2 = request.POST['password2']

            if str(pass_word)!=str(pass_word2):
                return render(request, "register.html", {"register_form": register_from, "msg": "密码不一致"})


            user_profile = UserProfile()
            user_profile.username=user_name
            user_profile.email = user_name
            # 调用加密函数
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name,"register")

            return render(request,"login.html")
        else:
            return render(request, "register.html", {"register_form": register_from})
    pass


class ForgetPwdView(View):
    # 找回密码
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form })
    def post(self,request):

        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST["email"]

            validata_email=UserProfile.objects.filter(email=email)

            if validata_email:
                send_register_email(email, "forget")
                return render(request, "send_success.html")

            return render(request, "forgetpwd.html", {'msg':"邮箱不存在"})

        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})



class ResetView(View):
    # 重置密码view
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                current_code=record.code

                #链接是否有效
                if record.is_useful:
                    return render(request,"password_reset.html",{"email":email,"current_code":current_code})
                else:
                    return render(request, "login.html",{'msg':"验证码过期"})
        else:
            return render(request,"active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    # 修改密码
    def post(self, request):
        loginCaptch = LoginCaptch()
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST["password1"]
            pwd2 = request.POST["password2"]

            email = request.POST["email"]
            #当前的验证链接
            current_code = request.POST["current_code"]

            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email,'is_NotSame':True, "msg": "密码不一致"})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            #验证完后取消验证链接
            EmailVerifyModeLl = EmailVerifyRecord.objects.get(code=current_code)
            EmailVerifyModeLl.is_useful=False
            EmailVerifyModeLl.save()

            return render(request, "login.html",{"loginCaptch":loginCaptch})
        else:
            email = request.POST["email"]
            return render(request, "password_reset.html", {"email": email, "modify_form":modify_form})


def page_nont_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code=404
    return response

def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response