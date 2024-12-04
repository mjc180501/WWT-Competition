from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, PostForm
from .models import Post

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = RegistrationForm()
    return render(request, 'polls/register.html', {'form': form})

@login_required
def post_page(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('homepage')
    else:
        form = PostForm()
    return render(request, 'polls/post.html', {'form': form})

def homepage(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'polls/homepage.html', {'posts': posts})
