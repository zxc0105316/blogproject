from blog.models import Post,Category
from django import templatetags
from django import template



register = template.Library()
# 最新文章模块标签
# 实现提取最新的指定数量的文章的功能，默认为5
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]
# 归档模块标签
# 实现按时间归档的功能 month是归档的时间精度，order是排序的方式
@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')


#分类模块标签

@register.simple_tag
def get_categorys():
    return Category.objects.all()