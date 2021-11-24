from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, UserForm, UserProfileInfoForm
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = Post.published.all()
    return render(request,'flexxi/index.html', {'posts':posts} )

def computer(request):
    return render(request,'flexxi/computer.html' )

def	blog(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 8) # 8 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # If page is not an integer deliver the first page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # If page is out of range deliver last page of results
    return	render(request, 'flexxi/blog.html', { 'page':page, 'posts':posts, 'tag':tag })

def	detail(request, year, month, day, post):
    
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    
    comments = post.comments.filter(active=True)  # List of active comments for this post
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)  # A comment was posted
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # Create Comment object but don't save to database yet
            new_comment.post = post  # Assign the current post to the comment
            new_comment.save()  # Save the comment to the database
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'flexxi/detail.html', {'post':post, 'comments':comments, 'new_comment':new_comment, 'comment_form':comment_form, 'similar_posts':similar_posts })

def enquiries(request):
    return render(request, 'flexxi/enquiries.html')

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('got it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'flexxi/signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Inactive account!")
        else:
            print("Login attempt failed!")
            print("Username: {} and password: {} were used!".format(username,password))
            return HttpResponse("Invalid username and/or password!")
    else:
        return render(request, 'flexxi/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))