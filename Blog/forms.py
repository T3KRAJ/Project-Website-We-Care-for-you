from django import forms
from Blog.models import BlogPost, Images, Comment


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    content = forms.TextInput()
    category = forms.Select()

    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'category',)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )