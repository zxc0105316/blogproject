from django.shortcuts import render
from django.http import HttpResponse
from .models import  Post,Category
from django.shortcuts import get_object_or_404
import markdown
from comments.forms import CommentForm
# Create your views here.

# def index(request):
#     return render(request,'blog/index.html',context={
#         'title':'我的博客首页',
#         'welcome':'欢迎访问我的博客主页',
#     })


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    print(post_list)
    return render(request,'blog/index.html',context={'post_list':post_list})



def details(request,pk):
    # print("ok")
    post  =  get_object_or_404(Post,pk=pk)
    # print("1")
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc',
                                  ])
    #
    form = CommentForm()
    # 获取文章下的所有评论
    comment_list = post.comment_set.all()
    # 将文章、表单、以及文章下的评论列表作为模板变量传给detail.html模块，以便渲染相应数据
    context = {
        'post':post,
        'form':form,
        'comment_list':comment_list,
    }
    return render(request,'blog/details.html',context=context)



def archive(request,year,month):

    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    )
    return render(request,'blog/index.html',context={'post_list':post_list})



def category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=category)
    return render(request,'blog/index.html',context={'post_list':post_list})


