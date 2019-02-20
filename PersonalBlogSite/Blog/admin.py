from django.contrib import admin

from .models import User,Class,Article,Comment

# Register my own models.
class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_title','article_simpledesc','article_class','article_publisher','article_pubdate','article_content']
    list_display = ('article_title','article_class','article_publisher','article_pubdate')
    list_filter = ['article_pubdate','article_class']
    search_fields = ['article_title']

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name','user_email','user_isadmin')

admin.site.register(Article,ArticleAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Class)
admin.site.register(Comment)