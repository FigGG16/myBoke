__author__ = 'FigGG'
__date__ = '2017/8/4 下午8:11'

from django.conf.urls import url,include
from Category.views import ArticleView
from Category.views import ArticleClassView
from Category.views import ArticleDetailView,AddComentsView,AddCommentVote
from Category.views import ArticleApi

urlpatterns = [
# 模版继承 --课程机构首页
    url(r'^list/$', ArticleClassView.as_view(), name="Article_class"),

    url(r'^class/(?P<category_list_id>\d+)/$', ArticleView.as_view(), name="category_class"),

    url(r'^show/(?P<category_list_id>\d+)/$', ArticleDetailView.as_view(), name="category_detail"),

    url(r'^comments/$', AddComentsView.as_view(), name="add_comments"),

    url(r'^comment_vote/$',AddCommentVote.as_view(),name="add_fav"),

    #评论API
    url(r'^api/$', ArticleApi.as_view(), name="json_api"),

]