from django.contrib import admin
from .models import Image, Comment
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created',]
    list_filter = ['created']

admin.site.register(Image, ImageAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'body', 'created']
    list_filter = ['created']

admin.site.register(Comment, CommentAdmin)

