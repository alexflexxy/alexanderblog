from django.db import models
from django.utils import timezone 
from django.contrib.auth.models	import User
from django.urls import	reverse
from taggit.managers import TaggableManager


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class PublishedManager(models.Manager):	    # Creating and defining custom manager
    def	get_queryset(self):	
        return	super(PublishedManager,	self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_OPTIONS	= (('draft', 'Draft'),('published', 'Published'),)				
    title	=	models.CharField(max_length=350)				
    slug	=	models.SlugField(max_length=400, unique_for_date='publish')
    author	=	models.ForeignKey(User,	on_delete=models.CASCADE, related_name='blog_posts')
    photo   =   models.ImageField(upload_to='media/', null=True, blank=True)
    story	=	models.TextField()
    publish	=	models.DateTimeField(default=timezone.now)
    created	=	models.DateTimeField(auto_now_add=True)	
    updated	=	models.DateTimeField(auto_now=True)				
    status	=	models.CharField(max_length=10,	choices=STATUS_OPTIONS,	default='draft')

    class Meta:								
        ordering = ('-publish',)

    def	__str__(self):								
        return	self.title

    tags = TaggableManager()

    # Adding the custom	manager to the Post model
    objects	= models.Manager()  # Default manager.
    published =	PublishedManager()  # Created custom manager

    # Building canonical urls for Post objects
    def	get_absolute_url(self):
        return	reverse('flexxi:detail',
                        args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)