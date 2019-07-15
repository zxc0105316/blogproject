from django.conf.urls import url
from . import views
# 这个app_name 命名空间的声明是告诉其他应用这个urls.py
# 文件是在这个应用下使用的。
app_name = 'comments'
urlpatterns = [

    url(r'^comment/post/(?P<post_pk>[0-9]+)/$',views.post_comment,name='post_comment'),
]