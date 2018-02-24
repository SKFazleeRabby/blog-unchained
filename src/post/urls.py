from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.PostCreate.as_view(), name='create'),
    path('<int:post_id>/edit/', views.PostUpdate.as_view(), name='update'),
    path('<int:post_id>/delete/', views.PostDelete.as_view(), name='delete')
]
