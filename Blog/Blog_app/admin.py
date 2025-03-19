from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug', 'publish', 'author', 'status']
    search_fields=['title', 'body']
    date_hierarchy='publish'
    ordering= ['status', 'publish']
    prepopulated_fields= {'slug': ('title',)}
    show_facets = admin.ShowFacets.ALWAYS