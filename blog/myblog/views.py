# coding:utf8
from django.shortcuts import render, redirect
from django.conf import settings
import logging
from .models import *
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.db import connection
from forms import *
from django.db.models import Count
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password

logger = logging.getLogger('myblog.views')


def global_setting(request):
    # 站点配置
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # 全局分类配置
    category_list = Category.objects.all()[1:6]
    # 全局广告配置
    ad_list = Ad.objects.all()
    # 全局标签云配置
    tag_list = Tag.objects.all()
    # 全局外部链接配置
    link_list = Links.objects.all()[:5]
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by(
        '-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    click_list = Article.objects.all().order_by('-click_count')[:6]
    station_is_recommend_list = Article.objects.filter(is_recommend='is_recommend')

    return locals()


# Create your views here.
def index(request):
    try:
        article_list = Article.objects.all()
        article_list = get_paginator(request, article_list)
        print 'jadsfjkljadskfl'
        # print Article.objects.distinct_date()
    except Exception as e:
        logger.error(e)
    return render(request, 'Home.html', locals())


def get_paginator(request, article_list):
    paginator = Paginator(article_list, 4)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (PageNotAnInteger, EmptyPage, InvalidPage):
        article_list = paginator.page(1)
    return article_list


def tag(request):
    try:
        tag = request.GET.get('tag', None)
        article_list = Article.objects.filter(tag__name__icontains=tag)
        article_list = get_paginator(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'tag.html', locals())


def article(request):
    id = request.GET.get('id', None)
    try:
        try:
            article = Article.objects.get(pk=id)
        except Exception as e:
            return render(request, 'failure.html', {"reason": '没有找到对应的页面'})

        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})

        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)

    except Exception as e:
        logger.error(e)
    return render(request, 'article.html', locals())


def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment.objects.create(username=comment_form.cleaned_data['author'],
                                             email=comment_form.cleaned_data['email'],
                                             url=comment_form.cleaned_data['url'],
                                             content=comment_form.cleaned_data['comment'],
                                             article_id=comment_form.cleaned_data['article'],
                                             user=request.user if request.user.is_authenticated()else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


def do_register(request):
    try:
        if request.method == 'POST':
            register_form = RegForm(request.POST)
            if register_form.is_valid():
                user = User.objects.create(username=register_form.cleaned_data['username'],
                                           email=register_form.cleaned_data['email'],
                                           url=register_form.cleaned_data['url'],
                                           password=make_password(register_form.cleaned_data['password']))
                user.save()

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': register_form.errors})
        else:
            register_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())


def do_login(request):
    try:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': login_form.errors})
                return redirect(request.POST.get('source_url'))
            else:
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


def category(request):
    try:
        cid = request.GET.get('id',None)
        try:
            category = Category.objects.filter(pk = cid)
        except:
            return render(request,'failure.html',{'reason':'找不到对应分类'})
        article_list = Article.objects.filter(category=category)
        article_list = get_paginator(request,article_list)
    except Exception as e:
        logger.error(e)
    return render(request,'category.html',locals())