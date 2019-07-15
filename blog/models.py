from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    "分类的表"
    name = models.CharField(max_length=100)



    def __str__(self):
        return self.name


class Tag(models.Model):
    "标签的表"
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
class Post(models.Model):
    "文章的数据库表"

    #文章标题
    title = models.CharField(max_length=70)

    #文章正文
    body = models.TextField()

    #文章的创建时间和最后一次修改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    #文章摘要 ,可以不填 ,blank=True表示允许空值
    excerpt = models.CharField(max_length=200,blank=True)

    # 分类和标签的关联字段
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)


    # 文章作者，这里User 是从django.contrib.auth.models导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，
    # User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        print(self.pk)
        return reverse("blog:details",kwargs={'pk': self.pk})



    class Meta:
        # 在模型中指定排序
        # 为了让文章（Post）按发布时间逆序排列，即最新发表的文章排在文章列表的最前面，我们对返回的文章列表进行了排序，即各个视图函数中都有类似于
        # Post.objects.all().order_by('-created_time')
        # 这样的代码，这导致了很多重复
        # ordering属性用来指定文章排序方式，['-created_time']
        # 指定了依据哪个属性的值进行排序，这里指定为按照文章发布时间排序，
        # 且负号表示逆序排列。列表中可以用多个项，
        # 比如ordering = ['-created_time', 'title'] ，那么首先依据
        # created_time排序，如果created_time相同，则再依据title排序。
        # 这样指定以后所有返回的文章列表都会自动按照Meta中指定的顺序排序，
        # 因此可以删掉视图函数中对文章列表中返回结果进行排序的代码了。
        ordering = ['-created_time']