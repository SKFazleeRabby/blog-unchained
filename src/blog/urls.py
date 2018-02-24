from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/<int:post_id>/', views.BlogDetailView.as_view(), name='blog-detail')
]
