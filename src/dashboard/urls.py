from django.urls import path, include
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('user/profile/', views.ProfileView.as_view(), name='profile'),
    path('user/profile/edit/', views.ProfileEditView.as_view(), name='profile-edit'),
    path('comments/', views.CommentView.as_view(), name='comments'),
    path('comments/<int:comment_id>/delete', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('password/change/', views.ChangePassword.as_view(), name='change-password'),
    path('settings/', views.SettingView.as_view(), name='settings'),
    path('posts/', include('post.urls')),
    path('categories/', include('category.urls'))
]
