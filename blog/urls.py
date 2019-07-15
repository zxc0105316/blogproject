# blog/urls.py


from django.conf.urls import url

from . import views
# 视图函数命名空间 做隔离
app_name = 'blog'
urlpatterns = [

    url(r'^$',views.index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.details,name='details'),
    url(r'archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archive,name='archive'),
    url(r'category/(?P<pk>[0-9]+)/$',views.category,name='category'),
]