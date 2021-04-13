from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from  rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)

#Import For class based views
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import  ListAPIView
from rest_framework.authentication import TokenAuthentication
from operator import attrgetter

#for search 
from rest_framework.filters import SearchFilter ,OrderingFilter

#models and serialilzers
from accounts.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializers


@api_view(['GET',])
@permission_classes((AllowAny, ))#allows acess for any type of user
def api_detail_blog_view(request ,slug):

    try:
        blog_post = BlogPost.objects.get(slug = slug)
    except BlogPost.DoesNotExist:
        return  Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BlogPostSerializers(blog_post)
        return  Response(serializer.data)


@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))#allow acess to only authorized user 
def api_update_blog_view(request ,slug):

    try:
        blog_post = BlogPost.objects.get(slug = slug)
    except BlogPost.DoesNotExist:
        return  Response(status = status.HTTP_404_NOT_FOUND)

    user = request.user

    if blog_post.author != user:
        return Response({'response' : 'You are not allowed to modify'})

    if request.method == "PUT":
        serializer = BlogPostSerializers(blog_post , data = request.data)
        data = {}
        if serializer.is_valid():
            blog = serializer.save()
            data["success"] = "Updates Sucessfully"
            data['title'] = blog.title
            data['body'] = blog.body
            data['image'] = blog.image.url
            return Response(data=data)
        return  Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated , ))#allow acess to only authorized user 
def api_delete_blog_view(request ,slug):

    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return  Response(status = status.HTTP_404_NOT_FOUND)

    user = request.user

    if blog_post.author != user:
        return Response({'response' : 'You are not allowed to delete'})

    if request.method == "DELETE":
        operation = blog_post.delete()
        data = {} 
        if operation:
            data["success"] = "Deleted Sucessfully"
        else:
            data["failure"] = "Delete Failed"
        return  Response(data=data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))#allow acess to only authorized user 
def api_create_blog_view(request):

    account = request.user
    blog_post = BlogPost(author=account)

    if request.method == "POST":
        serializer = BlogPostSerializers(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



#class based views coz they are easier 
#pagination sahit ko list view
class ApiBlogListView(ListAPIView):
    queryset = sorted(BlogPost.objects.all(), key =attrgetter('date_updated'), reverse =True ) 
    serializer_class = BlogPostSerializers
    authentication_classes = (TokenAuthentication, ) #Allowany garda token chaindaina tyei ni samjhina lai rakhdeyko 
    permission_classes = (AllowAny, ) #since it is list dont forget to add comma
    pagination_class = PageNumberPagination    
    #author__name is the way to specify certain item of foreign key feild to retreive that item 


class ApiBlogSearchView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializers
    # authentication_classes = (TokenAuthentication, ) #since it is list dont forget to add comma
    permission_classes = (AllowAny, ) #since it is list dont forget to add comma
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter ,OrderingFilter)
    search_fields = ('title' , 'body' ,'author__name' )
    ordering_fields = ('-date_updated','title') #order k k ko adhar ma garna paine bhanera
    ordering = ('-date_updated',) #order gardinxa

    #author__name is the way to specify certain item of foreign key feild to retreive that item 






