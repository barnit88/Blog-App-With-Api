from rest_framework import serializers
from blog.models import BlogPost


class BlogPostSerializers(serializers.ModelSerializer):

    email = serializers.SerializerMethodField('get_email_from_author')
    name = serializers.SerializerMethodField('get_name_from_author')

    class Meta:
        model = BlogPost
        fields = ['title' , 'body' , 'image' , 'date_updated' ,'email' ,'name']

    def get_email_from_author(self,blog_post):
        email = blog_post.author.email
        return email
    
    def get_name_from_author(self,blog_post):
        name = blog_post.author.name
        return name




