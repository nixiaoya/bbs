#coding=utf-8

from django.template.loader import get_template
from django.http import HttpResponse,HttpResponseRedirect
from PIL import Image,ImageDraw,ImageFont

from users.views import login_required
from users.functions import getSession
from main.models import *

def Home(request):
    catList = Category.objects.filter(father_category=0).order_by('id')
    articleList = Article.objects.order_by("create_at")
    
    user = getSession(request)
    context = {
            'article_list':articleList,
            'cat_list':catList,
            'user':user,
        }
    template = get_template("main/home.html")
    html = template.render(context,request) 
    return HttpResponse(html)

def ArticleList(request,actType="xx"):
    try:
        getCategory = Category.objects.get(name = actType)
    except Category.DoesNotExist:
        return HttpResponseRedirect("error404")
    articleList = Article.objects.filter(category = getCategory).order_by("create_at")
    user = getSession(request)
    context = {
            "select_category":getCategory,
            "article_list":articleList,
            'user':user,
    }
    template = get_template("main/article_list.html")
    html = template.render(context,request) 
    return HttpResponse(html)

def ArticleDetail(request,artID=None):
    try:
        article = Article.objects.get(id = artID)
    except Article.DoesNotExist:
        return HttpResponseRedirect("error404")
        
    user = getSession(request)
    context = {
            "article":article,
            'user':user,
    }

    template = get_template("main/article_detail.html")
    html = template.render(context,request) 
    return HttpResponse(html)

@login_required
def ArticleNew(request):
    user = getSession(request)
    context = { 
        "user":user
        }
    template = get_template("main/new.html")
    html = template.render(context,request) 
    return HttpResponse(html)
