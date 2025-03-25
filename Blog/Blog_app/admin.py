from django.contrib import admin
from .models import Post
from.models import Comment

# Register your models here.
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug', 'publish', 'author', 'status']
    search_fields=['title', 'body']
    date_hierarchy='publish'
    ordering= ['status', 'publish']
    prepopulated_fields= {'slug': ('title',)}
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display=['name', 'email','post','created', 'updated', 'active']
    search_fields=['name', 'email', 'body']
    list_filter=['created','updated', 'active']