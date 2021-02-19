from django.contrib import admin
from .models import Article, Comment,Like, Tag
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Tag)