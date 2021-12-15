from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    """Model that defines a blog post"""
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name="blog_posts", blank=True)
    
    def total_likes(self):
        print(self.likes.count())
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single',args=(str(self.id)))

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE )
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    website_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('user_profile',args=(str(self.id)))
