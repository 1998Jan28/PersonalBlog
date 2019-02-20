from django.urls import path
from . import views

app_name = 'Blog'  # 命名空间

urlpatterns =[
    path('',views.index,name='index'),
    path('detail/<int:article_id>/',views.detail,name='detail'),
    path('comment/',views.comment,name='comment'),
    path('classes/',views.classes,name='classes'),
    path('archive/',views.archive,name='archive'),
    path('message/',views.message,name='message'),
    path('about/',views.about,name='about'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
]