# coding: utf-8
from django.contrib import admin

# Register your models here.

from .models  import Comment   	# 从数据库中引入一个类数据

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'text', 'created_time']


admin.site.register(Comment, CommentAdmin)        # 引入Comment
