from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from post.forms import PostForm
from post.models import Post


class IndexView(ListView):
    model = Post
    template_name = 'post/all.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.is_admin:
            return self.model.objects.filter(user=self.request.user).select_related('category').order_by('-created_at')
        return self.model.objects.all().select_related('category')


class PostCreate(SuccessMessageMixin, CreateView):
    form_class = PostForm
    template_name = 'post/post_form.html'
    extra_context = {
        'button_name': 'PUBLISH',
        'form_title': 'Create Post'
    }
    success_url = reverse_lazy('dashboard:post:index')
    success_message = "Your Post Has Been Created Successfully."

    def get_success_message(self, cleaned_data):
        return messages.success(self.request, self.success_message, extra_tags=self.object.id)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'
    pk_url_kwarg = 'post_id'
    extra_context = {
        'button_name': 'UPDATE',
        'form_title': 'Update Post'
    }
    success_url = reverse_lazy('dashboard:post:index')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_admin and self.request.user != self.get_object().user:
            return redirect('dashboard:post:index')
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)


class PostDelete(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('dashboard:post:index')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_admin and self.request.user != self.get_object().user:
            return redirect('dashboard:post:index')
        return super(PostDelete, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

