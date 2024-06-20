from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('content/' , views.content_data , name = 'content'),
    path('content/<int:id>/', views.content_data, name='content-detail'), 
    path('search/', views.search_content, name='content-search'), 
    path('create/' , views.create_content , name='create'),

]+static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)