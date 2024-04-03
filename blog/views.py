import datetime
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import PostForm
from .models import Post, Category, Tag, Subscribe, Comment, Photo


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2 + count % 2
    return {'cats1': all[:half], 'cats2': all[half:]}


def get_tags():
    tag = Tag.objects.all()
    return {'tags': tag}


def get_comments():
    comment = Comment.objects.all()
    return {'comments': comment}


def get_photos():
    photos = Photo.objects.all()
    return {'photos': photos}


def index(request):
    posts = Post.objects.all().order_by("-published_date")
    newPost = Post.objects.get(pk=1)

    # posts = Post.objects.filter(title__contains="python")
    # posts = Post.objects.filter(published_date__year=2023)
    # posts = Post.objects.filter(content__startswith="Lorem")
    # posts = Post.objects.filter(category__name__iexact="it")
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {"posts": posts, 'newPost': newPost}
    context.update(get_tags())
    context.update(get_categories())
    context.update(get_comments())
    context.update(get_photos())
    return render(request, 'blog/index.html', context)


def post(request, title=None):
    post = get_object_or_404(Post, title=title)
    context = {"post": post}
    context.update(get_tags())
    context.update(get_categories())
    context.update(get_comments())
    context.update(get_photos())
    return render(request, 'blog/post.html', context)


def about(request):
    return render(request, 'blog/about.html', context={})


def contact(request):
    return render(request, 'blog/contact.html', context={})


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def tag(request, tag=None):
    t = get_object_or_404(Tag, tag=tag)
    posts = Post.objects.filter(tag=t).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_tags())
    return render(request, 'blog/index.html', context)


@login_required
def comm(request):
    now = datetime.datetime.now()
    comm = request.POST.get('comm')
    post_id = request.POST.get('id')
    user = request.user
    Comment.objects.create(name=comm, published_date=now, post=Post.objects.get(pk=post_id), user=user)
    return HttpResponseRedirect(f'/blog/post/{Post.objects.get(pk=post_id)}')


def comment(request, comment=None):
    comm = get_object_or_404(Comment, comment=comment)
    posts = Post.objects.filter(comment=comm).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_comments())
    return render(request, 'blog/index.html', context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())
    context.update(get_tags())
    return render(request, 'blog/index.html', context)


def email(request):
    mail = request.POST.get('mail')
    Subscribe.objects.create(email=mail)
    return HttpResponseRedirect('/')


@login_required
def create(request):
    now = datetime.datetime.now()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now
            post.user = request.user
            post.save()
            for tag_id in request.POST.getlist('tags'):
                try:
                    tag = Tag.objects.get(id=tag_id)
                    post.tags.add(tag)
                except Tag.DoesNotExist:
                    raise NotFound()
            for photo_id in request.POST.getlist('image'):
                try:
                    photo = Photo.objects.get(id=photo_id)
                    post.image.add(photo)
                except Photo.DoesNotExist:
                    raise NotFound()

    form = PostForm()
    context = {"form": form}
    context.update(get_categories())
    context.update(get_tags())
    context.update(get_photos())
    return render(request, 'blog/create.html', context)


def profile(request):
    return render(request, 'blog/profile.html')


def update_profile(request):
    return render(request, 'blog/update_profile.html')


def accept_update_profile(request):
    user_avatar = request.POST.get('user_avatar')
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user_id = int(request.POST.get('id'))
    user = User.objects.get(pk=user_id)

    user.blog_user_info.avatar = os.path.join(os.path.abspath(__file__), '../../uploads/photos', user_avatar)
    user.blog_user_info.save()

    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password = make_password(password)
    user.save()
    return HttpResponseRedirect('/')


def registration_user(request):
    return render(request, 'blog/registration_user.html')


def create_user(request):
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = make_password(request.POST.get('password'))
    User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    return HttpResponseRedirect('/')

