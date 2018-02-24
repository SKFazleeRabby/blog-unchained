from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from category.models import Category


class IndexView(ListView):
    model = Category
    template_name = 'category/all.html'
    context_object_name = 'categories'


class CategoryCreate(CreateView):
    model = Category
    template_name = 'category/category_form.html'
    fields = ['name']
    extra_context = {'extras': {
        'title': 'Create Category',
        'button_name': 'Create'
        }
    }


class CategoryUpdate(UpdateView):
    model = Category
    template_name = 'category/category_form.html'
    fields = ['name']
    extra_context = {'extras': {
        'title': 'Update Category',
        'button_name': 'Update'
    }
    }
    pk_url_kwarg = 'category_id'


class CategoryDelete(DeleteView):
    model = Category
    pk_url_kwarg = 'category_id'
    success_url = reverse_lazy('dashboard:category:index')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

