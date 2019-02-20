from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.utils import timezone

from .models import Article,Comment,Class,User

import markdown

# Create my own views.

# 首页
def index(request):
    # 获取所有博文，并按时间倒序排序
    article_list = Article.objects.all().order_by('-article_pubdate')
    paginator = Paginator(article_list, 10)   #Django分页类
    try:
        page = request.GET['page']
        article = paginator.page(page)  # 获取对应页数的文章
    except PageNotAnInteger:
        article = paginator.page(1)   #如果page不是整数，返回第一页
    except EmptyPage:
        article = paginator.page(paginator.num_pages)  #如果是空页，则返回最后一页
    except KeyError:
        article = paginator.page(1)
    # 获取最近的5条评论
    latest_comment_list = Comment.objects.all().order_by('-comment_date')[:5]
    # 上下文字典
    context = {
        'article_list':article,
        'latest_comment_list':latest_comment_list,
    }
    return render(request,'Blog/index.html',context)

# 文章详情页
def detail(request,article_id):
    # 根据id获取对应博文
    article = get_object_or_404(Article,pk=article_id)
    # 最近5条评论
    latest_comment_list = Comment.objects.all().order_by('-comment_date')[:5]
    # 将文字内容转换为markdown格式
    article.article_content = markdown.markdown(article.article_content.replace("\r\n", '  \n'),
                        extensions=['markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',],safe_mode=True,enable_attributes=False)
    # 获取该篇博文的评论
    article_comment = Comment.objects.filter(comment_article__id=article_id).order_by('-comment_date')
    comment_reply = {}
    comment_num = 0
    for comment in article_comment:
        if comment.comment_father:
            pass
        else:
            comment_reply[comment] = Comment.objects.filter(comment_father__id=comment.id).order_by('-comment_date')
            comment_num = comment_num + 1
    context = {
        'article':article,
        'latest_comment_list':latest_comment_list,
        'article_comment':comment_reply,
        'comment_num':comment_num,
    }
    return render(request,'Blog/detail.html',context)

# 评论
def comment(request):
    if request.method == 'POST':
        try:
            comment_content = request.POST['content']
            comment_date = timezone.now()
            comment_user = get_object_or_404(User,pk=request.POST['user_id'])
            comment_article = get_object_or_404(Article,pk = request.POST['article_id'])
            if request.POST['father_id']=="-1":     # 对文章的评论
                comment = Comment(comment_content=comment_content,comment_date=comment_date,comment_user=comment_user,comment_article=comment_article)
                comment.save()
                return JsonResponse({'msg':'评论成功'})
            else:
                comment_father = get_object_or_404(Comment,pk = request.POST['father_id'])
                comment = Comment(comment_content=comment_content,comment_date=comment_date,comment_user=comment_user,comment_article=comment_article,comment_father=comment_father)
                comment.save()
                return JsonResponse({'msg':'回复成功'})
        except (KeyError,User.DoesNotExist,Article.DoesNotExist):
            return JsonResponse({'msg':'评论错误'})
    if request.method == 'GET':
        return render(request,'Blog/index.html') 

# 按类别分类
def classes(request):
    # 获取所有分类
    class_list = Class.objects.all()
    # 保存每个类对应文章的字典
    class_article = {}
    # 遍历所有分类，并获取每个类别的博文
    for cl in class_list:
        class_article[cl] = Article.objects.filter(article_class__id=cl.id).order_by('-article_pubdate')
    # 最近5条评论
    latest_comment_list = Comment.objects.all().order_by('-comment_date')[:5]
    context = {
        'class_article':class_article,
        'latest_comment_list':latest_comment_list,
    }
    return render(request,'Blog/classes.html',context)

# 归档，按月份分类
def archive(request):
    # 获取所有年份,使用集合保存年份
    year_set = set()
    article_list = Article.objects.all()
    for article in article_list:
        year_set.add(article.article_pubdate.year)
    year_list=list(year_set)
    year_list.sort(reverse = True)
    # 获取每年的博文
    year_article = {}
    for year in year_list:
        year_article[year] = Article.objects.filter(article_pubdate__year=year).order_by('-article_pubdate')
    # 最近5条评论
    latest_comment_list = Comment.objects.all().order_by('-comment_date')[:5]
    
    context = {
        'year_article':year_article,
        'latest_comment_list':latest_comment_list,
    }
    return render(request,'Blog/archieve.html',context)

# 留言
def message(request):
    # 最近5条评论
    latest_comment_list = Comment.objects.all().order_by('-comment_date')[:5]

    context = {
        'latest_comment_list':latest_comment_list,
    }
    return render(request,'Blog/message.html',context)

# 关于
def about(request):
    # 最近5条评论
    latest_comment_list = Comment.objects.all().order_by('-comment_date')[:5]

    context = {
        'latest_comment_list':latest_comment_list,
    }
    return render(request,'Blog/about.html',context)

# 登陆
def login(request):
    if request.method == 'POST':        # if request.is_ajax()     采用ajax向后台发送消息
        try:
            email = request.POST['email']     # 邮箱
            password = request.POST['password']     # 密码
            user = User.objects.get(user_email=email,user_password=password)    # 获取该用户对象，这里需要使用get，而非filter
        except (KeyError,User.DoesNotExist):
            return JsonResponse({'msg':'邮箱或密码错误！'})
        if user:
            # 如果用户存在且密码正确则登陆成功
            return JsonResponse({'msg':'success','email':email,'username':user.user_name,'userid':user.id})
    if request.method == 'GET':
        return render(request,'Blog/login.html')    # GET请求说明用户刚进入登陆界面
    

# 注册
def register(request):
    if request.method == 'POST':
        try:
            name = request.POST['nickname']    # 昵称
            email = request.POST['email']     # 邮箱
            password = request.POST['password']     # 密码
            check_email = len(list(User.objects.filter(user_email=email)))
            if check_email==0:
                user = User(user_name=name,user_email=email,user_password=password,user_isadmin=False)
                user.save()
                return JsonResponse({'msg':'success'})
            else:
                return JsonResponse({'msg':'该邮箱已被注册！'})
        except KeyError:
            return render(request,'Blog/register.html')
    if request.method == 'GET':
        return render(request,'Blog/register.html')   # GET请求说明用户刚进入注册界面
