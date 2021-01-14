from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from requests import post

from .models import Post
from .forms import PostModelForm, PostForm, CommentForm

# comment 등록
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)

    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html',{'form':form})


@login_required
# Post 삭제
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@login_required
# Post 수정 : Form 사용
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #         작성자
            post.author = User.objects.get(username=request.user.username)
            #         게시일, 글 게시 날짜
            post.published_date = timezone.now()
            #     실제 등록됨
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
# Post 등록 : Form 사용
def post_new(request):
    if request.method == 'POST':
        # 실제 등록 처리하기
        form = PostForm(request.POST)
        if form.is_valid():
            # form 데이터가 clena한 상태
            print(form.cleaned_data)
            post = Post.objects.create(author=User.objects.get(username=request.user.username),
                                       title=form.cleaned_data['title'],
                                       text=form.cleaned_data['text'],
                                       published_date=timezone.now())

            return redirect('post_detail', pk=post.pk)


    else:
        # 등록하는 빈 폼을 보여준다.
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
# Post 등록 ModelForm 사용
def post_new(request):
    if request.method == 'POST':
        #     실제 등록 처리하기
        form = PostModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #         작성자
            post.author = User.objects.get(username=request.user.username)
            #         게시일, 글 게시 날짜
            post.published_date = timezone.now()
            #     실제 등록됨
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 등록하는 빈 폼을 보여준다.
        form = PostModelForm()
    return render(request, 'blog/post_edit.html', {'form': form})


# post 상세정보

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# Post 목록

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

    # 현재날짜보다 작거나 같은 값을 가져오고 어센딩 해라

    # 템플릿을 연결해주는 역할

    # Post 목록
    def post_response(request):
        name = 'Django'
        response = HttpResponse(f'<h2>Hello {name}</h2>', content_type="text/html")
        response.write(f'<h2>Hello {name}</h2>')
        response.write(f'<p>HTTP Method : {request.method}</p>')
        response.write(f'<p>HTTP ConentType : {request.content_type}</p>')
        # return HttpResponse(f'''<h2>Hello{name}</h2><p>HTTP METHOD : {request.method}</p>''')

        return response
