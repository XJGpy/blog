# coding: utf-8
from django.conf.urls import url   	# 导入django的url
from . import views					# 导入当前文件夹下的视图函数

app_name = 'blog'					#

urlpatterns = [						# 关联网址url与视图函数
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
	url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
	url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
	url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
	#url(r'^search/$', views.search, name='search'),
	
	url(r'^about/$', views.about, name='about'),
	url(r'^contact/$', views.contact, name='contact'),
	]

