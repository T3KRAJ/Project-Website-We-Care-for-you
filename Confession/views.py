from django.shortcuts import render, redirect, get_object_or_404, reverse
from Confession.models import ConfessionPost
from django.contrib import messages
from core.models import Profile
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class ConfessionPostList(ListView):
    queryset = ConfessionPost.objects.filter(status=1).order_by('-created_on')
    template_name = 'confession/confessions.html'
    paginate_by = 10

class CreateConfessionPost( LoginRequiredMixin, CreateView):
    model = ConfessionPost
    fields = ['title', 'content', 'display_name', 'category']
    success_url = "/confessions/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = int(1)
        return super().form_valid(form)


def confessionpost_detail(request, slug):
    post = get_object_or_404(ConfessionPost, slug=slug)
    comments = post.comments.filter(active=True, parent__isnull=True)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    return render(request,
                  'confession/confessionpost_detail.html',
                  {'confessionpost' : post,
                   'is_liked' : is_liked,
                   })

class CPUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ConfessionPost
    fields = ['title', 'content', 'display_name']
    success_url = ''
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or post.display_name:
            return True
        return False


class CPDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ConfessionPost
    success_url = '/confessions/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or post.display_name:
            return True
        return False

@login_required
def like_confessionpost(request):
    post = get_object_or_404(ConfessionPost, id=request.POST.get('confessionpost_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():          
        post.likes.remove(request.user)
        is_liked = False  
    else:
        post.likes.add(request.user)
        is_liked = True
    return redirect(post.get_absolute_url())
