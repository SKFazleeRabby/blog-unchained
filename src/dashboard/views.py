from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DetailView, TemplateView, FormView, ListView, DeleteView

from account.models import UserDetails, User
from dashboard.forms import ProfileEditForm, ChangePasswordForm
from post.models import Comments


class IndexView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        return render(request, self.template_name)


class SettingView(View):
    template_name = 'dashboard/settings.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileView(TemplateView):
    template_name = 'dashboard/profile.html'


class ProfileEditView(FormView):
    template_name = 'dashboard/profile_form.html'
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse('dashboard:profile')

    def get_form(self, form_class=ProfileEditForm):
        try:
            user_details = UserDetails.objects.get(user_id=self.request.user)
            return form_class(instance=user_details, **self.get_form_kwargs())
        except UserDetails.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super(ProfileEditView, self).form_valid(form)


class ChangePassword(FormView):
    template_name = 'dashboard/change_password_form.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('dashboard:profile')

    def get_form(self, form_class=ChangePasswordForm):
        try:
            user = User.objects.get(pk=self.request.user.id)
            return form_class(instance=user, **self.get_form_kwargs())
        except User.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.instance)
        return super(ChangePassword, self).form_valid(form)


class CommentView(ListView):
    model = Comments
    template_name = 'dashboard/comment.html'
    context_object_name = 'comments'

    def get_queryset(self):
        query = super(CommentView, self).get_queryset()
        if not self.request.user.is_admin:
            return query.select_related('post').select_related('user__userdetails').filter(post__user_id=self.request.user)
        return query.select_related('post').select_related('user__userdetails').all()


class CommentDeleteView(DeleteView):
    model = Comments
    pk_url_kwarg = 'comment_id'
    success_url = reverse_lazy('dashboard:comments')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.is_admin and self.object.post.user != self.request.user:
            return redirect('dashboard:comments')
        return super(CommentDeleteView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

