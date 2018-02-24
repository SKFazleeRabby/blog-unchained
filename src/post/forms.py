from django import forms

from category.models import Category
from post.models import Post, Comments


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=5)
    body = forms.CharField(widget=forms.Textarea, min_length=10)
    category = forms.ModelChoiceField(queryset=Category.objects, empty_label='-- Select Category --')
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'images', 'draft', 'featured', 'published']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['content']

    def save(self, commit=False):
        return super(CommentForm, self).save(commit=True)

