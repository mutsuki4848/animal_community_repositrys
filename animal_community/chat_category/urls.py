from django.urls import path
from . import views

app_name = 'chat_category'

urlpatterns = [
    path('create_theme', views.create_theme, name='create_theme'),
    path('list_themes', views.list_themes, name='list_themes'),
    path('edit_theme/<int:id>', views.edit_theme, name='edit_theme'),
    path('delete_theme/<int:id>', views.delete_theme, name='delete_theme'),
    path('post_comments/<int:theme_id>', views.post_comments, name='post_comments'),
    path('post_delete/<int:id>', views.post_delete, name='post_delete'),
    path('save_comment', views.save_comment, name='save_comment'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
]