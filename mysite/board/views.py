from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Follow

from django.conf import settings

def index(request):
  users = User.objects.all()
  if not request.user.is_authenticated:
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
  followings = request.user.following.all()
  posts = []
  for following in followings:
    user = following.user_to
    user_posts = Post.objects.filter(user=user)[:5]
    for t in user_posts:
      posts.append(t)
  context = {
    'user': request.user,
    'posts': posts,
    'users': users
  }
  return render(request, 'board/index.html', context)

def logout_user(request):
    logout(request)
    return redirect('board:index')

def signup(request):
    if request.method == 'POST':
        # validate user, save to db, redirect
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save user
            form.save()
            # log user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            # redirect
            return redirect('board:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required()
def compose_post(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    users = User.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        # validate
        if form.is_valid():
            new_post = form.save(commit=False)
            # add current_user id
            new_post.user = user
            # save db
            new_post.save()
            # redirect
            return redirect('board:index', current_user.id)
    else:
        form = PostForm()
    context = {
        'form' : form,
        'users': users
    }
    return render(request, 'board/compose_post.html', context)

# post page, shows the post and all its comments
def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    users = User.objects.all()
    comments = post.comments
    context = {
        'post': post,
        'comments': comments,
        'current_user': request.user,
        'users': users
    }
    # add comment as the current user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
    else:
        form = CommentForm()
    context['comment_form'] = form
    return render(request, 'board/post.html', context)

@login_required()
def user(request, user_id):
    current_user = request.user
    user = get_object_or_404(User, pk=user_id)
    users = User.objects.all()
    posts = user.posts.all()[:20]
    context = {
        'current_user': current_user,
        'user': user,
        'posts': posts,
        'users': users
    }
# is the current user already following page's user
    already_following = Follow.objects.filter(user_from=current_user, user_to=user_id).exists()
    context['is_following'] = already_following
    if request.method == 'POST':
        if already_following:
            #unfollow
            follow = Follow.objects.get(user_from=current_user, user_to=user_id)
            follow.delete()
        else:
            #follow
            follow = Follow(user_from=current_user, user_to=user)
            follow.save()
        return redirect('board:user', user_id)
    return render(request, 'board/user.html', context)