from django.db import models
from django.utils import timezone

from account.models import User
from category.models import Category


class PostManager(models.Manager):
    def active(self):
        return super(PostManager, self).filter(draft=False).filter(published__lte=timezone.now()).order_by('-published')

    def featured(self):
        return super(PostManager, self).filter(draft=False).filter(featured=True).filter(published__lte=timezone.now())[:5]

    def all(self):
        return super(PostManager, self).order_by('-created_at')


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    body = models.TextField(blank=False, null=False, default='images/default.png')
    images = models.ImageField(upload_to='images/posts', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    published = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now=True)

