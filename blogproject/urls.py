"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from blog.feeds import AllPostsRssFeed

# use Django server /media/ files
from django.conf import settings




urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'', include('blog.urls')),     	# 将应用下的视图函数路径包含在工程中，让其识别
	url(r'', include('comments.urls')),     # 将应用下的视图函数路径包含在工程中，让其识别
	
	# 记得在顶部引入 AllPostsRssFeed
    url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),
	
	# 搜索引擎
	url(r'^search/', include('haystack.urls')),
	
	# 编辑框
	url(r'^ueditor/', include('DjangoUeditor.urls' )),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)