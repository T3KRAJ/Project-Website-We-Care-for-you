from django.db import models
import os
from datetime import datetime
from django.contrib.humanize.templatetags import humanize
from django.shortcuts import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
CATEGORY = (
    ('LO', 'Love'),
    ('BU', 'Business'),
    ('CU', 'Culture'),
    ('LI', 'Lifestyle'),
    ('TE', 'Tech'),
    ('SP', 'Sports'),
    ('PO', 'Politics'),
    ('TR', 'Travel'),
    ('FU', 'Fun'),
    ('FE', 'Feeling'),
    ('FA', 'Fashion'),
    ('ED', 'Education'),
    ('HE', 'Health'),
    ('NA', 'Nature'),
    ('OT', 'Other')
)

def user_directory_path(instance,filename):
    base_name = os.path.basename(filename)
    name,ext = os.path.splitext(base_name)

    return "blog/user/"+ str(instance.author.id) + "/"+ str(instance.id)+ "/"+"IMG_"



class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    updated_on = models.DateTimeField(auto_now= True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="bloglikes")
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def get_date(self):
        return humanize.naturaltime(self.created_on)

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={
            'slug':self.slug
        })

    @property
    def total_likes(self):
        return self.likes.count()

def get_unique_slug(sender, instance, **kwargs):
    num = 1
    slug = slugify(instance.title)
    unique_slug = slug
    while BlogPost.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    instance.slug=unique_slug
pre_save.connect(get_unique_slug,sender=BlogPost)


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments_on_blog')
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_user')
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # manually deactivate inappropriate comments from admin site
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        # sort comments in chronological order by default
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)

    def get_date(self):
        return humanize.naturaltime(self.created)
    
    @property
    def total_comments(self):
        return self.likes.count()