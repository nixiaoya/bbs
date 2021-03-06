#coding=utf-8

from django.template.loader import get_template
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

from Main.models import Category
from User.forms import UserForm
from User.models import *
from functions import *

def Login(request):
	'''
	显示登陆页面
	'''
	catList = Category.objects.order_by('id')
	context = {
		'cat_list':catList,
		}
	template = get_template("user/login.html")
	html = template.render(context,request)
	return HttpResponse(html)

def Register(request):
	'''
	显示注册页面
	'''
	catList = Category.objects.order_by('id')
	context = {
		'cat_list':catList,
		}
	template = get_template("user/register.html")
	html = template.render(context,request)
	return HttpResponse(html)

def UserActive(request):
	'''
	账户激活
	'''
	email_token = str(request.GET.get('token','').strip())
	catList = Category.objects.order_by('id')
	result = "success"
	context = {}
	context["cat_list"] = catList

	try:
		user = User.objects.get(token=email_token)
	except:
		context["get_token"] = False
	else:
		context["get_token"] = True
		if user.active:
			context["info"] = u"该账户已激活"
		else:
			user.set_active()
			context["info"] = u"账户激活成功"
	template = get_template("user/active.html")
	html = template.render(context,request)
	return HttpResponse(html)

##-------- Ajax --------
def getChaptcha(request):
	'''
	获取验证码
	'''
	img = captcha()
	img.gen_img()
	request.session["verifycode"] = img.strs
	buf = StringIO.StringIO()
	img.img.save(buf,'gif')
	return HttpResponse(buf.getvalue(),'image/gif')

def ChapchaMatch(getChaptcha,request):
	sessionChaptch = request.session["verifycode"]
	if getChaptcha.lower() == sessionChaptch.lower():
		return True
	else:
		return False

def checkChapcha(request):
	getChaptcha = request.POST.get("chapcha","").strip()
	context = {}
	context["match"] = ChapchaMatch(getChaptcha,request)
	return JsonResponse(context)

def unameAvailableCheck(request):
	'''
	检查注册新用户的用户名是否可用
	'''
	context = {}
	getUsername = request.POST.get('username')
	user_obj = User.objects.filter(username = getUsername)
	if user_obj:
		context['success'] = True
	else:
		context['success'] = False
	return JsonResponse(context)

def postRegister(request):
	'''
	提交注册信息
	'''
	userform = UserForm(request)
	context = {}

	if userform.is_valid():
		user = userform.save()
		try:
			user.sendMail("register")
		except:
			user.delete()
			context["success"] = False
			context["error"] = "send email failed !"
		else:
			setSession(request,user)
			context["success"] = True
	else:
		context["success"] = False
		context["error"] = userform.error
	return JsonResponse(context)

def postLogin(request):
	'''
	提交登陆信息
	'''
	username = request.POST.get("username","").strip()
	password = request.POST.get("password","").strip()
	chapcha = request.POST.get("validcode","").strip()
	context = {}

	chapcha_match = ChapchaMatch(chapcha,request)

	try:
		user = User.objects.get(username = username)
	except User.DoesNotExist:
		context["status"] = 0
	else:
		if user.active:
			if user.check_password(password):
				context["status"] = 1
			else:
				context["status"] = 0
		else:
			context["status"] = 2
	return JsonResponse(context)






