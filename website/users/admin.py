from django.contrib import admin

from users.models import User 

class User_admin(admin.ModelAdmin):
	list_display=("username","email","active","is_login")
admin.site.register(User,User_admin)
