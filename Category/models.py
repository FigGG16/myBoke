from django.db import models
from users.models import  UserProfile
from datetime import datetime
from DjangoUeditor.models import UEditorField
# Create your models here.

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
#CK富文本
from ckeditor.fields import RichTextField

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    # user = models.ForeignKey(UserProfile, verbose_name=u"用户",null=True,blank=True)
    title = models.CharField('标题', max_length=70)
    # body = UEditorField(u'课程详情',width=600, height=400, imagePath="courses/ueditor/", filePath="courses/ueditor/",default='')
    # body =RichTextField()
    body=MarkdownxField()
    
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length=54, blank=True, null=True,
                                help_text="可选，如若为空将摘取正文的前54个字符")
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)

    category = models.ForeignKey('CategoryList', verbose_name='分类',
                                 null=True,
                                 on_delete=models.SET_NULL)

    @property
    def formatted_markdown(self):

        return markdownify(self.body)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u"文章"
        verbose_name_plural = verbose_name
        ordering = ['-last_modified_time']

    def get_cate_name(self):
        return self.category.name




class CategoryList(models.Model):
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"文章分类"
        verbose_name_plural = verbose_name



class ArticleComments(models.Model):
    "文章评论"
    user = models.ForeignKey(UserProfile,verbose_name=u"用户")
    Article= models.ForeignKey(Article,verbose_name=u"文章")
    comments = models.TextField(verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    Comment_Digg=models.CharField("评论点赞id",max_length=500,default='')
    Comment_Bury=models.CharField("评论反对id",max_length=500,default='')
    ReplyComent_id = models.IntegerField(verbose_name=u"回复评论ID",default=None)

    class Meta:
        verbose_name = u"文章评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_Comment_Digg_count(self):
          if self.Comment_Digg.strip(',').split(',')==['']:
            return 0
          else:
            return len(self.Comment_Digg.strip(',').split(','))
