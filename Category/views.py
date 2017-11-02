from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from .models import CategoryList,Article,ArticleComments

from .models import UserProfile
from django.db.models import Q

#API设置
from django.core import serializers
from django.utils.encoding import force_text
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view


import re
import json

from urllib.parse import quote
import string

# class LazyEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, YourCustomType):
#             return force_text(obj)
#         return super(LazyEncoder, self).default(obj)

class ArticleApi(View):
    def get(self, request):
        data = serializers.serialize("json",Article.objects.all())
        print(data)

        s = json.loads(serializers.serialize("json",Article.objects.all()))


        return JsonResponse(s, safe=False)

def get_index(request):

    obj = serializers.serialize("json",Article.objects.all())
    data = serializers.serialize("json", obj)

    return Response(data)

class ArticleView(View):
    def get(self,request,category_list_id):
        category_Artcles=Article.objects.filter(category_id=int(category_list_id))
        CategoryList_name=CategoryList.objects.get(id=int(category_list_id))
        # 取出所有新评论
        New_comment = ArticleComments.objects.all().order_by("-add_time")[:3]

        #取出所有评论
        comment_count=ArticleComments.objects.all()

        return render(request,"Art_mian_show.html",{
            "category_Artcles": category_Artcles,
            "CategoryList_name":CategoryList_name,
            "New_comment":New_comment,
            "comment_count": comment_count,
        })

class ArticleClassView(View):
    def get(self,request):

        topped_Artcles_all=None
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            # 课程搜索                              i代表不区分大小写
            category_Artcles_all = Article.objects.filter(
                Q(title__icontains=search_keywords) | Q(body__icontains=search_keywords))
        else:
            # 根据添加时间在新随笔显示
            category_Artcles_all = Article.objects.filter(topped=False).order_by("-created_time")
            #获取全部的置顶笔记
            topped_Artcles_all=Article.objects.filter(topped=True).order_by("-created_time")


        #取出所有新评论
        New_comment=ArticleComments.objects.all().order_by("-add_time")[:3]

        #取出所有评论
        comment_count=ArticleComments.objects.all()

        #对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(category_Artcles_all, 4, request=request)
        Artcles_all = p.page(page)

        return render(request, "Art_main_list.html", {
            "New_comment":New_comment,
            "category_Artcles_all":Artcles_all,
            "comment_count":comment_count,
            "topped_Artcles_all":topped_Artcles_all
        })


class ArticleDetailView(View):

    def get(self,request,category_list_id):
        Article_count=Article.objects.count()
        #计算当前文章的上下文章
        if int(category_list_id) ==Article_count and int(category_list_id)!=1:
            next_Artcles =Article.objects.get(id=(int(category_list_id) - 1))
            pre_Artcles= None

        elif int(category_list_id)==1 and  Article_count!=int(category_list_id):
            pre_Artcles = Article.objects.get(id=(int(category_list_id) +1))
            next_Artcles = None

        elif Article_count>=2:
            # category_Artcles = Article.objects.get(id=int(category_list_id))
            next_Artcles = Article.objects.get(id=(int(category_list_id) + 1))
            pre_Artcles = Article.objects.get(id=(int(category_list_id) - 1))
        else:
            pre_Artcles = None
            next_Artcles = None
        #判断是否对应的文章
        category_Artcles = Article.objects.get(id=int(category_list_id))


        #提取内容中的目录
        line = category_Artcles.body
        regex_str = "##([\u4E00-\u9FA5 a-z 0-9#.*￥|/\|&]+?\s)"
        match_obj = re.match(regex_str, line, re.M)
        Article_list = re.findall(regex_str, line, re.M)


        # 取出所有新评论
        New_comment = ArticleComments.objects.all().order_by("-add_time")[:3]
        #取出文章中评论
        all_comments = ArticleComments.objects.filter(Article_id=category_list_id)


        return render(request,"Art_detail.html",{

        "Artcles_Detail":category_Artcles,
        "all_comments":all_comments,
        "next_Artcles":next_Artcles,
        "pre_Artcles":pre_Artcles,
        "New_comment":New_comment,

        "Article_list":Article_list

        })

class AddComentsView(View):

    def post(self,request):
        if not request.user.is_authenticated():
            #没登录就返回json
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        Artcles_Detail_id = request.POST.get("Artcles_Detail_id",0)
        comments = request.POST.get('comments',"")


        click_Comment_id=request.POST.get('click_Comment_id',"")
        is_replyComent = re.findall(r"@(.+?)\n", comments)
        if click_Comment_id and is_replyComent!=[]:
            #回复评论者的的名称

            curr_comments=ArticleComments.objects.get(id=click_Comment_id)
            if is_replyComent[0]==curr_comments.user.username:
                if int(Artcles_Detail_id) > 0 and comments:
                    #获取最新的评论ID
                    Art_comments=ArticleComments.objects.order_by('-add_time')[1:][0].id+1;
                    curr_comments.ReplyComent_id=Art_comments
                    curr_comments.save()

                    articleComments = ArticleComments()
                    # 有多条数据或没有数据抛出异常
                    article = Article.objects.get(id=int(Artcles_Detail_id))

                    articleComments.Article = article

                    # 为回复内容加上<br>
                    com=comments[:len(curr_comments.user.username)+1]+"<br>"+comments[len(curr_comments.user.username)+1:]

                    articleComments.comments = com
                    articleComments.user = request.user
                    articleComments.ReplyComent_id = 0
                    articleComments.save()
                    return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"file","msg":"添加失败"}', content_type='application/json')



        if int(Artcles_Detail_id) >0 and comments:
            articleComments = ArticleComments()
            #有多条数据或没有数据抛出异常
            article = Article.objects.get(id=int(Artcles_Detail_id))

            articleComments.Article=article
            articleComments.comments=comments
            articleComments.user = request.user
            articleComments.ReplyComent_id=0
            articleComments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"file","msg":"添加失败"}', content_type='application/json')



class AddCommentVote(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)#目标的对象id。主键

        fav_type = request.POST.get('fav_type',0)#点赞/反对

        #判断用户是否登录,没登录就返回json
        if not request.user.is_authenticated():
            #没登录就返回json
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        #提取该评论的对象
        exit_records = ArticleComments.objects.get(id=fav_id)


        #返回str并转成list
        #ExistBury_user_id = exit_records.Comment_Bury.strip(',').split(',')
        ExistDigg_user_id =exit_records.Comment_Digg.strip(',').split(',')

        if  ExistDigg_user_id!=[''] :
            if int(fav_type)==1:
                for Digg in ExistDigg_user_id:
                    #如果支持已存在，已存在则取消
                    if int(Digg) == request.user.id:
                        ExistDigg_user_id.remove(Digg)
                        #转为字符串
                        exit_records.Comment_Digg=",".join(ExistDigg_user_id)
                        exit_records.save()
                        return HttpResponse('{"status":"success","msg":"取消支持"}', content_type='application/json')
                #如果不存在则插入
                exit_records.Comment_Digg = exit_records.Comment_Digg + ',' + str(request.user.id)
                exit_records.save()
                return HttpResponse('{"status":"success","msg":"已支持"}', content_type='application/json')
        else:
            exit_records.Comment_Digg = str(request.user.id)
            exit_records.save()
            return HttpResponse('{"status":"success","msg":"已支持"}', content_type='application/json')

        return HttpResponse('{"status":"fail","msg":"支持出错"}', content_type='application/json')



        # exit_records =ArticleComments.
        #
        # exit_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        #
        # if exit_records:
        #     #如果记录已经存在，则表示取消
        #     exit_records.delete()
        #     return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        # else:
        #     user_fav = UserFavorite()
        #     if int(fav_id) >0 and  int(fav_type)>0:
        #         user_fav.user = request.user
        #         user_fav.fav_id = int(fav_id)
        #         user_fav.fav_type = int(fav_type)
        #         user_fav.save()
        #         return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
        #     else:
        #         return HttpResponse('{"status":"success","msg":"收藏出错"}', content_type='application/json')