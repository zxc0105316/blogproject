from django.shortcuts import render,HttpResponse,redirect,reverse,get_object_or_404
from blog.models import Post
from .models import Comment
from .forms import  CommentForm

# Create your views here.


def post_comment(request,post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post,pk=post_pk)


    if request.method == 'POST':
        form  = CommentForm(request.POST)
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            # 将评论和被评论的文章进行关联
            comment.post = post
            # 最终将数据保存进数据库
            comment.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            # 这里的redirect(post)没有指定网页
            # 它会自动执行这个blog.models中Post模型中定义的get_absolute_url方法
            # 然后跳转到这个函数方法返回的URL
            return redirect(post)

            #这里说明一下这个redirect函数，
            # redirect既可以接收一个URL作为参数，
            # 也可以接收一个模型的实例作为参数（例如这里的post）。
            # 如果接收一个模型的实例，那么这个实例必须实现了get_absolute_url方法，
            # 这样redirect会根据get_absolute_url方法返回的URL值进行重定向。
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。

            comment_list = post.comment_set.all()
            # 另外我们使用了post.comment_set.all()来获取post对应的全部评论。
            # Comment和Post是通过ForeignKey关联的，回顾一下我们当初获取某个分类cate
            # 下的全部文章时的代码：Post.objects.filter(category=cate)。这里
            # post.comment_set.all()也等价于Comment.objects.filter(post=post)，即根据
            # post来过滤该post下的全部评论。
            context = {'post':post,
                        'form':form,
                        'comment_list':comment_list,}
            return render(request,'blog/details.html',context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)