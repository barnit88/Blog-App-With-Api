from blog.models import BlogPost
from blog.views import get_blog_queryset
from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage ,PageNotAnInteger , Paginator

# Create your views here.

BLOG_POSTS_PER_PAGE = 2

#Module for Home Screen View
def home_screen_view(request):
	# Empty Context
	context = {}    
	
	# Intially query is empty string
	query = ""
	
	if request.GET:
	
		# if request does not contain key as 'q' then  the second argument will be provided 
		# that means if therey is no key as 'q' in http request then the query output will be
		# second parameter of get
		query = request.GET.get('q',"")  
		context['query'] = str(query)
		
	
	# querying and displaying in sorted way 
	# key is defined to get specific column from table 
	# reverse equal to true ,reverses the date from latest 
	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	context['blogs'] = blog_posts   
	
	
	# Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)  
	
	context['blogs'] = blog_posts   
	return render(request, "home/home.html", context)
