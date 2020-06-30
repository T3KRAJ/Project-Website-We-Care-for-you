from django.shortcuts import render, redirect, get_object_or_404, reverse
from Confession.models import ConfessionPost, Comment
from django.contrib import messages
from core.models import Profile
from django.utils import timezone
from Confession.forms import CommentForm
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
    template_name = 'confession/confessionpost_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = int(1)
        return super().form_valid(form)


def confessionpost_detail(request, slug):
    post = get_object_or_404(ConfessionPost, slug=slug)
    comments = post.comments_on_confession.filter(active=True, parent__isnull=True)

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None

            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None


            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment_name = request.user
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.name = request.user

            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    return render(request,
                  'confession/confessionpost_detail.html',
                  {'confessionpost' : post,
                  'comments' : comments,
                   'is_liked' : is_liked,
                   'comment_form': comment_form
                   })

class CPUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ConfessionPost
    fields = ['title', 'content', 'display_name']
    success_url = ''
    template_name = 'confession/confessionpost_form.html'
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
    template_name = 'confession/confessionpost_confirm_delete.html'
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
