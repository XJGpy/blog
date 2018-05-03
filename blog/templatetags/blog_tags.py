# coding: utf-8

from django.db.models.aggregates import Count
from django import template
from ..models import Post, Category, Tag

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):   	# 获取5篇文章，按时间排序
	return Post.objects.all()[:num]

@register.simple_tag
def archives():					# 获取时间信息
	return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag			# 获取分类信息
def get_categories():
	#return Category.objects.all()
	return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag			# 获取标签信息
def get_tags():
	return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

