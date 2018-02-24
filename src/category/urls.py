from django.urls import path
from category import views

app_name = 'category'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CategoryCreate.as_view(), name='create'),
    path('<int:category_id>/edit/', views.CategoryUpdate.as_view(), name='update'),
    path('<int:category_id>/delete/', views.CategoryDelete.as_view(), name='delete')
]

