from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_list', views.post_list, name='post_list'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_post, name='create'),
    path('about/', views.about_page, name='about'),
    path('post/<int:pk>', views.delete_post, name='delete'),
    path('post/<int:pk>/comments/', views.comments_post, name='comments'),

]
