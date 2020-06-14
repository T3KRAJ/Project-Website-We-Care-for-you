from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from PIL import Image
from django.shortcuts import reverse
from Blog.models import BlogPost
from Confession.models import ConfessionPost


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    bio = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse("profileof", kwargs={
            'slug':self.user.username
        })

    def get_num_of_blogs(self):
        blogs = BlogPost.objects.filter(author=self.user)
        return blogs.count()

    def get_num_of_confessions(self):
        confessions = ConfessionPost.objects.filter(author=self.user)
        return confessions.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
