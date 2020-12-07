from django.shortcuts import render, redirect

# Create your views here.
from django.http.response import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm

@login_required()
def index(request):
    current_user = request.user
    return render(request, 'board/index.html', {'username': current_user.username})

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
def compose(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        # validate
        if form.is_valid():
            new_tweet = form.save(commit=False)
            # add current_user id
            new_tweet.user_id = current_user.id
            # save db
            new_tweet.save()
            # redirect
            return redirect('board:index')
    else:
        form = PostForm()
    return render(request, 'board/compose.html', {'form': form})
