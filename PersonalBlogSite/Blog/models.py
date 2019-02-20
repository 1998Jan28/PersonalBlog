from django.db import models

from mdeditor.fields import MDTextField

# Create my own models.

class User(models.Model):
    user_name = models.CharField('name',max_length = 50)
    user_password = models.CharField('password',max_length = 50)
    user_email = models.EmailField('email')
    user_isadmin = models.BooleanField('isadmin')
    def __str__(self):
        return self.user_name

class Class(models.Model):
    class_label = models.CharField('label',max_length = 20)
    class_description = models.CharField('description',max_length = 100)
    def __str__(self):
        return self.class_label

class Article(models.Model):
    article_title = models.CharField('title',max_length = 100)
    article_simpledesc = models.CharField('simple description',null=True,blank=True,max_length = 200)
    article_content = MDTextField('content')
    article_pubdate = models.DateTimeField('date published')
    article_publisher = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='publisher')
    article_class = models.ForeignKey(Class,null=True,blank=True,on_delete=models.CASCADE,verbose_name='class')
    def __str__(self):
        return self.article_title

class Comment(models.Model):
    comment_content = models.TextField('comment')
    comment_date = models.DateTimeField('date commented')
    comment_user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='comment user')
    comment_father = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,verbose_name='father comment')
    comment_article = models.ForeignKey(Article,null=True,on_delete=models.CASCADE,verbose_name='comment article')
    def __str__(self):
        return self.comment_content
