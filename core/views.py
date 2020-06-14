from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, DeactivateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView
from core.models import Profile
from Blog.models import BlogPost, Images
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

@login_required
def profileView(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    posts = BlogPost.objects.filter(author=user)
    # post_images = Images.objects.filter(post=posts[0])  #Incomplete (rendering of images in blogpost)
    context = {
        'user':user,
        'profile':profile,
        'posts':posts,
        # 'post_images':post_images,
    }
    return render(request, 'profile.html', context)




@login_required
def updateProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile', username = request.user)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'updateprofile.html', context)



