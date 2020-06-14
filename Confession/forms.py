from django import forms
from Confession.models import ConfessionPost, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )