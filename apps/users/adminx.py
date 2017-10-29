__author__ = 'FigGG'
__date__ = '2017/8/1 上午1:55'

import xadmin
from  xadmin import views

from .models import EmailVerifyRecord,Banner


#主题设置
class BaseSetting(object):
    enable_themes = True
    #use_bootswatch=True

class GlobalSetting(object):
    site_title = "FXbloc后台管理系统"
    site_footer = "FX在线网"
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    #邮箱验证码的各种属性设置
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']

   # pass
class BannerAdmin(object):

    list_display = ['title', 'image', 'url', 'index','add_time']

    search_fields =['title', 'image', 'url', 'index']

    list_filter =['title', 'image', 'url', 'index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)