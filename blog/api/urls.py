from django.urls import path
from blog.api.views import (
    api_detail_blog_view,
    api_update_blog_view,
    api_delete_blog_view,
    api_create_blog_view,
    ApiBlogListView,
    ApiBlogSearchView
)
app_name = 'blog-api'

urlpatterns = [
    path('<slug>/' , api_detail_blog_view , name = 'detail-api'),
    path('<slug>/update/' , api_update_blog_view , name = 'update-api'),
    path('<slug>/delete/' , api_delete_blog_view , name = 'delete-api'),
    path('create' , api_create_blog_view , name = 'create-api'),
    path('list' , ApiBlogListView.as_view() , name = 'list-api'), #bcoz it is class based view
    path('search' , ApiBlogSearchView.as_view() , name = 'search-api'),
]