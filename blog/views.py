import logging

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Post, Comment

from .forms import PostNormalForm
from .forms import PostForm

from instablog.sample_exceptions import HelloWorldError


logger = logging.getLogger('django')

"""
template tags
    {% .... %}
template variable
    {{ ... }}
"""

def list_posts(request):
    logger.warning('경고 경고')
    # raise HelloWorldError('무슨 문젤까?')
    # return render(request, 'hello.html')
    per_page = 2
    page = request.GET.get('page', 1)
    posts = Post.objects.all()

    pg = Paginator(posts, per_page)

    try:
        contents = pg.page(page)
    except PageNotAnInteger:
        contents = pg.page(1)
    except EmptyPage:
        contents = []

    #템플릿 컨텍스트 생성
    ctx = {
        'posts' : contents
    }

    return render(request, 'list.html', ctx)


def detail_posts(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    ctx = {
        'post' : post,
        'comments' : comments
    }
    return render(request, 'detail.html', ctx)


@login_required
def create_posts(request):
    if not request.user.is_authenticated():
        raise Exception('누구세요?')

    form = PostForm()
    ctx = {
        'form' : form,
    }
    if request.method == 'GET':
        return render(request, 'edit.html', ctx)
    elif request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid() is True:
            data = form.save(commit=False) # 아래 내용들을 한줄로 표현할수 있다.
            data.user = request.user
            data.save()

            #리턴된 data 는 Model 클래스의 인스턴스임.

            # new_post = Post()
            # new_post.title = form.cleaned_data['title']
            # new_post.content = form.cleaned_data['content']
            # #new_post.full_clean()      #모델의 데이터들이 제대로 들어갔는지 확인한다.
            # new_post.save()

            url = reverse('blog:detail', kwargs={'pk' : data.pk})
            return redirect(url)

        else:
            ctx = {'form':form}

    # ctx = {}
    return render(request, 'edit.html', ctx)
