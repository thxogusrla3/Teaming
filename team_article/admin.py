from django.contrib import admin
from .models import ArticleFile, ArticleUrl
# Register your models here.
# admin.site.register(Article)
admin.site.register(ArticleFile)
# admin.site.register(ArticleImage)
admin.site.register(ArticleUrl)
# admin.site.register(Comment)