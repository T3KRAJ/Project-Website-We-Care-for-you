from django import forms
from Blog.models import BlogPost, Comment


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    content = forms.TextInput()
    category = forms.Select()

    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'category', 'image', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )