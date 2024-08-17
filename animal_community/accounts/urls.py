from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static  


app_name = 'accounts'

urlpatterns = [
    path('',views.home, name='home'),
    path('regist', views.regist, name='regist'),
    path('activate_user/<uuid:token>',views.activate_user, name='activate_user'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_edit', views.user_edit, name='user_edit'),
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('pet_regist/', views.pet_regist, name='pet_regist'),
    path('profile/pet/<int:pet_id>/', views.pet_profile, name='pet_profile'),
    path('delete_pet/<int:pet_id>', views.delete_pet, name='delete_pet'),
    path('pets/<int:pet_id>/edit/', views.pet_edit, name='pet_edit'),  # ペット編集へのリンク
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)