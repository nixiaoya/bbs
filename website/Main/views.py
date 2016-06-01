#coding=utf-8

from django.template.loader import get_template
from django.http import HttpResponse,HttpResponseRedirect
from PIL import Image,ImageDraw,ImageFont

from Main.models import *

def Home(request):	
	catList = Category.objects.filter(father_category=0).order_by('id')
	articleList = Article.objects.order_by("create_at")

	context = {
			'article_list':articleList,
			'cat_list':catList,
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
	context = {
		"select_category":getCategory,
		"article_list":articleList
	}
	template = get_template("main/article_list.html")
	html = template.render(context,request)	
	return HttpResponse(html)

def ArticleDetail(request,artID=None):
	try:
		article = Article.objects.get(id = artID)
	except Article.DoesNotExist:
		return HttpResponseRedirect("error404")
	context = {
		"article":article,
	}
	template = get_template("main/article_detail.html")
	html = template.render(context,request)	
	return HttpResponse(html)

def ArticleNew(request):
	context = {}
	template = get_template("main/new.html")
	html = template.render(context,request)	
	return HttpResponse(html)


