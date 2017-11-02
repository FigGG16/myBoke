"""myBoke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from users.views import LoginView
from django.views.generic import TemplateView
# from users.views import user_login
from users.views import RegisterView

#加载图片的URL
from django.conf.urls import url,include
from users.views import ForgetPwdView

from users.views import ModifyPwdView,ResetView
import xadmin

#激活
from users.views import ActiveUserView

from django.views.static import serve
from myBoke.settings import MEDIA_ROOT

from users.views import LogoutView

from Category.views import ArticleClassView

from myBoke.settings import STATIC_ROOT

urlpatterns = [

    url(r'^xadmin/', xadmin.site.urls),

    # url('^$', TemplateView.as_view(template_name="index.html"), name="index"),

    #加载首页
    url('^$', ArticleClassView.as_view(), name="index"),
    #登录界面
    url('^login/$',LoginView.as_view(),name="login"),
    #登出页面
    url('^logout/$', LogoutView.as_view(), name="logout"),
    #注册页面
    url('^register/$',RegisterView.as_view(),name="register"),
    #验证码
    url(r'^captcha/', include('captcha.urls')),
    #用户验证邮箱
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="user_active"),

    #找回密码
    url(r'forget/$', ForgetPwdView.as_view(), name="forget_pwd"),

    #重新设置密码邮箱
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    #修改密码
    url(r'modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    #加载静态文件目录
    url(r'media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
    #加载文章页
    url(r'Cate/', include('Category.urls',namespace="CateN")),

   #百度云富文本
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    #ck富文本
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^markdownx/', include('markdownx.urls')),

    # 配置全局404
    url(r'static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

]
#配置全局404页面
# handler404 = 'users.views.page_nont_found'
# handler500 = 'users.views.page_error'