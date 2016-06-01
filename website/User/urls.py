from django.conf.urls import *

urlpatterns = patterns('User.views',
	url(r'^login/$','Login'),
	url(r'^register/$','Register'),
	url(r'^active/$','UserActive'),

	#---- ajax ----
	url(r'^get_chaptcha/$','getChaptcha'),
	url(r'^uname_available/$','unameAvailableCheck'),
	url(r'^post_register/$','postRegister'),
	url(r'^post_login/$','postLogin'),
	url(r'^check_chapcha/$','checkChapcha'),
)
