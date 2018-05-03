# coding: utf-8

from django.contrib import admin

# Register your models here.

from .models  import Post, Category, Tag   	# 从数据库中引入三个类数据

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


admin.site.register(Post, PostAdmin)        # 引入Post
admin.site.register(Category)             	# 引入Category
admin.site.register(Tag)             		# 引入Tag
