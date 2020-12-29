from django.contrib import admin

# Register your models here.
from .models import Post, Follow, Comment

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Comment)