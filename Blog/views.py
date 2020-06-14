from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Blog.models import BlogPost, Images, Comment
from Blog.forms import PostForm, ImageForm, CommentForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class BlogPostList(ListView):
    queryset = BlogPost.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/blogs.html'  
    # incomplete (rendering of images in blogpost)
    paginate_by = 10



def createBlogPost(request):

    ImageFormSet = modelformset_factory(Images, form = ImageForm, extra=3)

    if request.method == 'POST':      
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        postForm = PostForm(request.POST)

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.author = request.user
            post_form.status = 1
            post_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(post=post_form, image=image)
                photo.save()
            
            messages.success(request,
                             "Posted!")
            return redirect("blog:posts")
        else:
            messages.error(request, "Some errors occured")
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'blog/create_blog_post.html',
                  {'postform': postForm, 'formset': formset})


@login_required
def blogpost_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments_on_blog.filter(active=True, parent__isnull=True)
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
                  'blog/blogpost_detail.html',
                  {'blogpost': post,
                   'comments': comments,
                   'is_liked':is_liked,
                   'comment_form': comment_form})

class BPUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content']
    success_url = ""

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class BPDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = '/blogs/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def like_blogpost(request):
    post = get_object_or_404(BlogPost, id=request.POST.get('blogpost_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():          
        post.likes.remove(request.user)
        is_liked = False  
    else:
        post.likes.add(request.user)
        is_liked = True
    return redirect(post.get_absolute_url())
        