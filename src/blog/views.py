from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import FormMixin

from category.models import Category
from post.forms import CommentForm
from post.models import Post, Comments


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'featured_posts'
    extra_context = {
        'categories': Category.objects.all()[:6]
    }

    def get_queryset(self):
        return self.model.objects.featured()


class BlogView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.active()


class BlogDetailView(FormMixin, DetailView):
    template_name = 'single.html'
    pk_url_kwarg = 'post_id'
    queryset = Post.objects.active().select_related('category').select_related('user').select_related('user__userdetails')
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:blog-detail', kwargs={'post_id': self.kwargs.get('post_id')})

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comments.objects.filter(post_id=self.kwargs.get('post_id')).order_by('-created').select_related('user').select_related('user__userdetails')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.object
        form.save()
        return super(BlogDetailView, self).form_valid(form)

