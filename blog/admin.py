from django.contrib import admin

from .models import Post
from .models import Comment


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', ]
    list_display_links = ['id', 'title']
    ordering = ['-id', 'created_at', ]
    inlines = [CommentInlineAdmin, ]
    search_fields = ['title', 'content', ]
    date_hierarchy = 'created_at'      #하이라키가 정리되는데 시간이 걸릴수 있다.
    list_filter = ['status', 'title']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
