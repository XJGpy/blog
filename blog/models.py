# coding: utf-8

from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# 添加编辑框
from DjangoUeditor.models import UEditorField

class Category(models.Model):                       # 文章类别，作为一个数据库表
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Tag(models.Model):                            # 文章标签，作为一个数据库表
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Post(models.Model):							# 文章（类），作为一个数据库表
	title = models.CharField(max_length=70)			# 文章标题
	
	def __str__(self):
		return self.title
	
	# 修改添加编辑框	
	#body = models.TextField()						# 文章内容
	body = UEditorField('内容', height=300, width=1000,
	default=u'', blank=True, imagePath="uploads/images/",
	toolbars='besttome', filePath='uploads/files/')
	
	created_time = models.DateTimeField()			# 文章发布时间
	modified_time = models.DateTimeField()	 		# 文章最后修改时间
	excerpt = models.CharField(max_length=200, blank=True) 	# 文章摘要，允许为空
	category = models.ForeignKey(Category, on_delete=models.CASCADE)			# 文章的类别，关联到Category类，一对多的关系
	tags = models.ManyToManyField(Tag, blank=True)	# 文章标签，关联到Tag类，并且是多对多的关系
	author = models.ForeignKey(User, on_delete=models.CASCADE)				# 文章作者，一对多的关系，关联类User
	views = models.PositiveIntegerField(default=0)	# 显示阅读量
	
	# 获取定义好的url reverse 第一个参数‘blog：detail’，匹配blog
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})
	
	class Mate:
		ordering = ['-created_time', 'title'] 
	
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])
		
	def save(self, *args, **kwargs):
		# 如果没有手写摘要
		if not self.excerpt:
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
				])
			self.excerpt = strip_tags(md.convert(self.body))[:54]
			
		super(Post, self).save(*args, **kwargs)



