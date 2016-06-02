from django.contrib import admin

from main.models import *

class Category_admin(admin.ModelAdmin):
	list_display=("name","chinese_name","father_category")
admin.site.register(Category,Category_admin)

class Article_admin(admin.ModelAdmin):
	list_display=("title","summary","author","commentCount","created_at")
	list_filter=("created_at","category")
	search_fields = ("title",)
admin.site.register(Article,Article_admin)

