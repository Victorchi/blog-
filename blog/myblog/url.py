from django.conf.urls import url
from myblog import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tag/$', views.tag, name='tag'),
    url(r'^article/$', views.article, name='article'),
    url(r'^comment/post$', views.comment_post, name='comment_post'),
    url(r'^login/$', views.do_login, name='login'),
    url(r'^logout/$', views.do_logout, name='logout'),
    url(r'^register/$', views.do_register, name='regiester'),
    url(r'^category/$', views.category, name='category'),
]
