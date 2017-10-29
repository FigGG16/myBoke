__author__ = 'FigGG'
__date__ = '2017/8/4 下午6:20'

import xadmin
from  xadmin import views
from markdownx.widgets import AdminMarkdownxWidget


from .models import CategoryList,Article,ArticleComments



class ArticleAdmin(object):
    list_display = [ 'title', 'body', 'created_time','last_modified_time','status','abstract','views','likes','topped','category']
    search_fields = ['STATUS_CHOICES', 'title','status','abstract','views','likes','topped','category']
    list_filter = ['title', 'body', 'created_time','last_modified_time','status','abstract','views','likes','topped','category']
    # style_fields = {"body": "ueditor"}
    formfield_overrides={'body': AdminMarkdownxWidget}



class CategoryListAdmin(object):
    list_display = ['name','created_time','last_modified_time']
    search_fields =['name']
    list_filter =['name','created_time','last_modified_time']


class ArticleCommentsAdmin(object):
    list_display = ['user','Article','comments','add_time']
    search_fields = ['user','Article']
    list_filter =['user','Article','comments','add_time']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(CategoryList, CategoryListAdmin)
xadmin.site.register(ArticleComments, ArticleCommentsAdmin)


