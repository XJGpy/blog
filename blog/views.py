# coding: utf-8
from django.shortcuts import render, get_object_or_404

# Create your views here.
import markdown
from django.http import HttpResponse
from .models import Post, Category, Tag
from comments.forms import CommentForm

from django.views.generic import ListView, DetailView    # 使用类视图函数

from django.db.models import Q

def index(request):
	#return HttpResponse("你好，世界！")
	#return render(request, 'blog/index.html', context={
	#				'title': '我的博客首页',
	#				'welcome':'欢迎访问我的博客首页',
	#				})
	#				
	post_list = Post.objects.all()#.order_by('-created_time')
	#comment_list = post_list.comment_set.all()
	#context = {	'post_list': post_list,
	#			'comment_list':comment_list,
	#			}
	return render(request, 'blog/index.html', context={'post_list': post_list})
	
def about(request):
	return render(request, 'blog/about.html', )
	
def contact(request):
	return render(request, 'blog/contact.html', )
	

def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.increase_views()                    # 获取阅读量
	post.body = markdown.markdown(post.body, # 语法高亮
								  extensions=[
									'markdown.extensions.extra',
									'markdown.extensions.codehilite',
									'markdown.extensions.toc',
									])
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {	'post':post,
				'form':form,
				'comment_list':comment_list
		}
	return render(request, 'blog/detail.html', context=context)
	#return render(request, 'blog/detail.html', context={'post':post})
	
def archives(request, year, month):
	post_list = Post.objects.filter(created_time__year=year,
									created_time__month=month,
									)
	return  render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate)
	return render(request, 'blog/index.html', context={'post_list': post_list})
	
# 搜索获取（关键字为标题和文章详情）	
def search(request):
	str = request.GET.get('str')
	error_msg = ''
	
	if not str:
		error_msg = "请输入关键词"
		return render(request, 'blog/index.html', {'error_msg':error_msg})
		
	post_list = Post.objects.filter(Q(title__icontains=str) | Q(body__icontains=str))
	return render(request, 'blog/index.html', {'error_msg':error_msg, 'post_list':post_list})
							

class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 3
	
	def get_context_data(self, **kwargs):

        # 首先获得父类生成的传递给模板的字典。
		context = super().get_context_data(**kwargs)
		
		# 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		
		# 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
		pagination_data = self.pagination_data(paginator, page, is_paginated)
		
		# 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
		context.update(pagination_data)
		
		# 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
		return context
		
	def pagination_data(self, paginator, page, is_paginated):
		# 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
		if not is_paginated:
			return {}
			
		# 当前页左边连续的页码号，初始值为空
		left = []
		# 当前页右边连续的页码号，初始值为空
		right = []
		 # 标示第 1 页页码后是否需要显示省略号
		left_has_more = False
		# 标示最后一页页码前是否需要显示省略号
		right_has_more = False
		first = False
		last = False
		page_number = page.number
		total_pages = paginator.num_pages
		page_range = paginator.page_range
		
		if page_number == 1:
			right = page_range[page_number:page_number + 2]
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
		elif page_number == total_pages:
			left = page_range[(page_number-3) if (page_number-3) > 0 else 0:page_number-1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number-3) if (page_number-3) > 0 else 0:page_number-1]
			right = page_range[page_number:page_number + 2] 
			
			if right[-1] < total_pages -1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
				
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		data = {
			'left':left, 
			'right':right,
			'left_has_more':left_has_more, 
			'right_has_more':right_has_more, 
			'first':first, 
			'last':last, 
			}
		return data
				
class CategoryView(IndexView):
	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)

class ArchivesView(IndexView):
	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchivesView, self).get_queryset().filter(created_time__year=year,created_time__month=month)

class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'
	
	def get(self, request, *args, **kwargs):
		response = super(PostDetailView, self).get(request, *args, **kwargs)
		self.object.increase_views()
		return response
	
	def get_object(self, queryset=None):
		post = super(PostDetailView, self).get_object(queryset=None)
		post.body = markdown.markdown(post.body,
										extensions=[
										'markdown.extensions.extra',
										'markdown.extensions.codehilite',
										'markdown.extensions.toc',
										])
		return post
		
	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
			'form':form, 
			'comment_list':comment_list
			})
		return context

class TagView(IndexView):
	def get_queryset(self):
		tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags=tag)
		
		

		
	


	
