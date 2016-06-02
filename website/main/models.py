#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.db import models
from users.models import User

import hashlib

#------ 新闻模块 -------

class Category(models.Model):
    name = models.CharField(max_length=32,unique=True)
    chinese_name = models.CharField(max_length=32,unique=True)
    father_category = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=258,blank=True,null=True)
    content =models.TextField()
    viewCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    category = models.ForeignKey('Category')

    def __unicode__(self):
        return self.title

#------ 评论模块 -------

class Comment(models.Model):
    content = models.CharField(max_length=256)
    create_at = models.DateTimeField(auto_now_add=True)
    vote = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    article = models.ForeignKey('Article')
    
    def add_vote(self):
        self.vote += 1
        self.save()

    def __unicode__(self):
        return self.author.username
