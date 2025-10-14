from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment, PostViews
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import PostForm, CommentForm
from django.db.models import Q, Count
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator


def post_list(request):
    query = request.GET.get('q')
    suggestions = []
    # for viral posts last 24 hrs by views
    
   
    

    all_posts = BlogPost.objects.order_by('-created_at')[:5]

    if query:
        suggestions = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )[:5]  # show top 5 matches

    # pagination
    paginator = Paginator(all_posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogapp/post_list.html', {
        'posts': all_posts,
        'query': query,
        'suggestions': suggestions,
        'trending_posts': trending_posts,
        'page_obj': page_obj,
    })






def post_detail(request, id,):
    post = get_object_or_404(BlogPost, id=id)

    # Fetch other posts (exclude current one)
    more_posts = BlogPost.objects.exclude(
        id=id)  # Adjust the number if needed

    pagenation_obj = Paginator(more_posts, 5)
    page_number = request.GET.get('page')
    page_obj = pagenation_obj.get_page(page_number)

    # track views from using ip address
    

    return render(request, 'blogapp/post_detail.html', {'post': post, 'page_obj': page_obj})


def about_page(request):
    return render(request, 'blogapp/about.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(
                username=username, password=password)
            login(request, user)
            return redirect('post_list')

    return render(request, 'blogapp/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'blogapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blogapp/create_post.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('post_list')


def comments_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.order_by('-created_at')
    comment_form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.blogpost = post
                comment.user = request.user
                comment.save()
                return redirect('comments', pk=pk)

    return render(request, 'blogapp/comments.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })
