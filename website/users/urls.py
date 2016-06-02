from django.conf.urls import *

urlpatterns = patterns('users.views',
	url(r'^login/$','Login'),
	url(r'^logout/$','Logout'),
	url(r'^register/$','Register'),
	url(r'^active/$','userActive'),

	#---- ajax ----
	url(r'^get_chaptcha/$','getChaptcha'),
	url(r'^uname_available/$','unameAvailableCheck'),
	url(r'^post_register/$','postRegister'),
	url(r'^post_login/$','postLogin'),
	url(r'^check_chapcha/$','checkChapcha'),
)
