from django.contrib import admin
from Blog.models import BlogPost, Comment

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

  
admin.site.register(BlogPost, BlogPostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'body')
    actions = ['block_comments', 'unblock_comments']

    def block_comments(self, request, queryset):
        queryset.update(active=False)

    def unblock_comments(self, request, queryset):
        queryset.update(active=True)